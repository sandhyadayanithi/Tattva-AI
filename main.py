import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, Request, HTTPException, Response, BackgroundTasks
import logging
from core.config import settings
from services.whatsapp_service import download_media, send_message, mark_as_read
import json
from ai.transcription import transcribe_audio
from ai.claim_extractor import ClaimExtractor
from ai.fact_checker import FactCheckerEngine
from services.firebase_service import firebase_service
from services.vector_service import vector_service
from models.message_model import MessageRecord
from services.ocr_service import OCRService

# --- CONFIGURATION (Managed in core.config) ---
# ---------------------

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tattva-AI Webhook API")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint for Meta API.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == settings.VERIFY_TOKEN:
            logger.info("WEBHOOK_VERIFIED")
            return Response(content=challenge, media_type="text/plain", status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    
    raise HTTPException(status_code=400, detail="Missing parameters")

@app.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Ultralight incoming webhook for WhatsApp messages. 
    Returns 200 immediately to Meta, processes in background.
    """
    try:
        body = await request.json()
        background_tasks.add_task(process_webhook_event, body)
        return Response(content="EVENT_RECEIVED", status_code=200)
    except Exception as e:
        logger.error(f"Webhook ingestion error: {str(e)}")
        # Always return 200 to avoid Meta retries if our parser fails
        return Response(content="OK", status_code=200)

async def process_webhook_event(body: dict):
    """
    Asynchronous background task to parse the Meta payload and trigger processing.
    """
    try:
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            sender_id = message.get("from")
                            message_id = message.get("id")
                            
                            # 1. Mark as read immediately (non-blocking)
                            asyncio.create_task(mark_as_read(message_id))
                            
                            # 2. Extract media/text and branch
                            msg_type = message.get("type")
                            
                            if msg_type == "audio":
                                audio = message.get("audio", {})
                                media_id = audio.get("id")
                                logger.info(f"Processing audio from {sender_id}")
                                asyncio.create_task(handle_voice_message_pipeline(sender_id, media_id))
                            elif msg_type == "image":
                                image = message.get("image", {})
                                media_id = image.get("id")
                                logger.info(f"Processing image from {sender_id}")
                                asyncio.create_task(background_process_image_and_reply(sender_id, media_id))
                            elif msg_type == "text":
                                text_body = message.get("text", {}).get("body", "")
                                logger.info(f"Processing text from {sender_id}")
                                asyncio.create_task(background_process_text_and_reply(sender_id, text_body))
                            else:
                                logger.info(f"Unsupported message type: {msg_type}")
                                asyncio.create_task(send_message(sender_id, "Please send a voice note, image, or text claim to verify."))
    except Exception as e:
        logger.error(f"Error in background event processor: {str(e)}")

@app.get("/messages/recent")
async def get_recent():
    """Debug route to see list of recent messages."""
    return firebase_service.get_recent_messages()

@app.get("/messages/user/{number}")
async def get_by_user(number: str):
    """Debug route to see messages from a specific user."""
    return firebase_service.get_messages_by_user(number)

@app.post("/test-claim-storage")
async def test_claim(claim: str, verdict: str, explanation: str):
    """Debug route to test caching a claim embedding."""
    dummy_result = {"verdict": verdict, "explanation": explanation}
    result = vector_service.store_claim(claim, dummy_result)
    return {"id": result, "status": "stored"}



async def handle_voice_message_pipeline(sender_id: str, media_id: str):
    """Downloads audio and triggers the full AI pipeline."""
    try:
        await send_message(sender_id, "Voice note received! 🎤 analyzing...")
        # 1. Download audio file
        audio_path = await download_media(media_id)
        if not audio_path:
            logger.error(f"Could not download audio for media_id {media_id}")
            await send_message(sender_id, "I encountered an error while trying to download your voice note.")
            return

        # 2. Trigger existing pipeline
        await background_process_audio_and_reply(sender_id, audio_path)

    except Exception as e:
        logger.error(f"Error in voice pipeline: {str(e)}")
        await send_message(sender_id, "An unexpected error occurred while processing your request.")

async def background_process_audio_and_reply(sender_id: str, audio_path: str):
    """Background task to run the AI pipeline for audio and send the result back via WhatsApp."""
    try:
        # 1. Run Pipeline (Whisper + Claim Extractor)
        pipeline_result = process_audio(audio_path)
        extracted_claim = pipeline_result.get("claim")
        detected_language = pipeline_result.get("language_name", pipeline_result.get("language", "English"))
        transcription = pipeline_result.get("text")
        
        import time
        time.sleep(3) # Increased pause for Free Tier stability
        await handle_claim_verification(sender_id, extracted_claim, transcription, audio_path, media_type="audio", language=detected_language)
        
    except Exception as e:
        logger.error(f"Error processing audio in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the audio.")

async def background_process_image_and_reply(sender_id: str, media_id: str):
    """Background task to run the AI pipeline for images and send the result back via WhatsApp."""
    try:
        await send_message(sender_id, "Image received! 📸 extracting text...")
        
        # 1. Download media
        image_path = await download_media(media_id)
        if not image_path:
            await send_message(sender_id, "Sorry, I couldn't download the image.")
            return

        # 2. Extract text from image
        logger.info(f"Running OCR on image: {image_path}")
        ocr_service = OCRService()
        extracted_text = ocr_service.extract_text(image_path)
        
        if not extracted_text:
            await send_message(sender_id, "I couldn't extract any text from the image.")
            return
            
        # 2. Extract claim from the OCR text
        import time
        time.sleep(1) # Quota stabilization
        logger.info(f"Extracting claim from OCR text...")
        extractor = ClaimExtractor()
        extraction_result = extractor.extract_claim(extracted_text)
        extracted_claim = extraction_result.get("claim")
        detected_language = extraction_result.get("language", "English")
        
        time.sleep(3) # Increased pause for Free Tier stability
        await handle_claim_verification(sender_id, extracted_claim, extracted_text, image_path, media_type="image", language=detected_language)
        
    except Exception as e:
        logger.error(f"Error processing image in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the image.")

async def background_process_text_and_reply(sender_id: str, text_content: str):
    """Background task to run the AI pipeline for plain text claims."""
    try:
        if not text_content:
            await send_message(sender_id, "Your message was empty. Please provide a claim to check.")
            return
            
        # 1. Extract claim from the text
        import time
        time.sleep(1) # Quota stabilization
        logger.info(f"Extracting claim from text...")
        extractor = ClaimExtractor()
        extraction_result = extractor.extract_claim(text_content)
        extracted_claim = extraction_result.get("claim")
        detected_language = extraction_result.get("language", "English")
        
        time.sleep(3) # Increased pause for Free Tier stability
        await handle_claim_verification(sender_id, extracted_claim, text_content, None, media_type="text", language=detected_language)
        
    except Exception as e:
        logger.error(f"Error processing text in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing your text claim.")

async def handle_claim_verification(sender_id, extracted_claim, full_text, file_path, media_type, language="English"):
    """Shared logic for fact-checking and reply sending."""
    if not extracted_claim:
        await send_message(sender_id, f"I couldn't extract a clear claim from your {media_type}.")
        return

    # 2. Fact-Check the claim
    engine = FactCheckerEngine()
    fact_check_result = engine.check_claim(extracted_claim, language=language)
    
    # Dual-language logic
    # Regional for WhatsApp
    verdict_reg = fact_check_result.get("verdict_reg", "Unknown")
    explanation_reg = fact_check_result.get("explanation_reg", "No explanation provided.")
    counter_message_reg = fact_check_result.get("counter_message_reg", "")
    
    # English for Firestore
    verdict_en = fact_check_result.get("verdict_en", "Unknown")
    explanation_en = fact_check_result.get("explanation_en", "No explanation provided.")
    counter_message_en = fact_check_result.get("counter_message_en", "")
    
    confidence = fact_check_result.get("confidence_score", 0.0)
    virality_score = fact_check_result.get("virality_score", 0)
    
    if fact_check_result.get("cached"):
        logger.info("Found similar claim in cache.")
        header = "🔍 *Found a Similar Cached Claim*"
    else:
        header = "✅ *Fact-Checked Result*"

    reply_text = (
        f"{header}\n\n"
        f"✅ *Verdict:* {verdict_reg}\n\n"
        f"📩 *Counter Message:* {counter_message_reg}\n\n"
        f"📝 *Explanation:* {explanation_reg}"
    )
    
    # 3. Store in Firestore (English ONLY)
    message_data = MessageRecord(
        user_number=sender_id,
        audio_file=file_path if media_type == "audio" else None,
        image_file=file_path if media_type == "image" else None,
        transcription=full_text, 
        claim=extracted_claim,
        verdict=verdict_en,
        explanation=explanation_en,
        confidence=confidence,
        virality_score=virality_score,
        counter_message=counter_message_en,
        raw_fact_check_response=fact_check_result
    )
    firebase_service.save_message(message_data)

    await send_message(sender_id, reply_text)


def process_audio(audio_path):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription and language detection...")
    whisper_result = transcribe_audio(audio_path)
    
    text = whisper_result["text"]
    language = whisper_result["language"]
    
    print(f"\nDetected Language: {language}")
    print(f"Input transcription:\n{text}")
    
    claim = text  # Default to raw text
    language_name = "English"
    if settings.USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        extraction_result = extractor.extract_claim(text)
        if extraction_result:
            claim = extraction_result.get("claim")
            language_name = extraction_result.get("language", "English")
            print(f"\nExtracted claim: {claim}")
            print(f"Detected language: {language_name}")
        else:
            print("\nFailed to extract claim.")
    else:
        print("\n2. [SKIPPED] Claim Extraction disabled. Using raw transcription as claim.")

    print("\n3. Running Fact Checker Engine...")
    import time
    time.sleep(3) # Mandatory pause to protect Gemini Free Tier quota
    fact_checker = FactCheckerEngine(use_llm=settings.USE_LLM)
    # This searches Tavily and optionally runs Gemini for the verdict.
    result = fact_checker.check_claim(claim, language=language_name)
    
    # Print the terminal output (filtering out the large body of evidence)
    output_result = {k: v for k, v in result.items() if k != "evidence_used"}
    print(json.dumps(output_result, indent=2, ensure_ascii=False))
    print("\n" + "-"*40 + "\n")
        
    return {
        "text": text,
        "language": language,
        "language_name": language_name,
        "claim": claim
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)
        
    process_audio(audio_file)
