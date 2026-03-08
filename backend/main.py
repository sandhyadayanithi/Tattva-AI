import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, Request, HTTPException, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
from core.config import settings
from services.whatsapp_service import download_media, send_message, mark_as_read, upload_media, send_audio_message
from services.elevenlabs_service import generate_regional_tts
import json
from ai.transcription import transcribe_audio
from ai.claim_extractor import ClaimExtractor
from ai.fact_checker import FactCheckerEngine
from services.firebase_service import firebase_service
from services.vector_service import vector_service
from models.message_model import MessageRecord
from services.ocr_service import OCRService
from utils.text_utils import normalize_transcript

# --- CONFIGURATION (Managed in core.config) ---
# ---------------------

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tattva-AI Webhook API")

@app.on_event("startup")
async def startup_event():
    """
    Runs on server startup. Seeds Firestore with mock data if not already initialized.
    """
    try:
        from seed_firestore import seed_data
        logger.info("Server starting up... Checking and seeding Firestore if necessary.")
        # Run seeding in a thread to prevent blocking main loop during large batch writes
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, seed_data)
        logger.info("Startup seeding check complete.")
    except Exception as e:
        logger.error(f"Error during startup seeding: {e}")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint for Meta WhatsApp API.
    """

    params = request.query_params

    # Accept both dot and underscore versions (tunnels sometimes rewrite them)
    mode = params.get("hub.mode") or params.get("hub_mode")
    token = params.get("hub.verify_token") or params.get("hub_verify_token")
    challenge = params.get("hub.challenge") or params.get("hub_challenge")

    logger.info(f"Webhook verification attempt: mode={mode}, token={token}, challenge={challenge}")

    if not mode or not token or not challenge:
        raise HTTPException(status_code=400, detail="Missing parameters")

    # strip() protects against accidental whitespace
    if mode == "subscribe" and token.strip() == settings.VERIFY_TOKEN.strip():
        logger.info("WEBHOOK_VERIFIED")
        return Response(content=challenge, media_type="text/plain", status_code=200)

    raise HTTPException(status_code=403, detail="Verification failed")

@app.get("/api/claims")
async def get_all_claims():
    """
    Endpoint for the dashboard to fetch all fact-checked claims from Firestore.
    """
    try:
        messages = firebase_service.get_recent_messages(limit=50)
        
        # Remap Firestore MessageRecord to Dashboard Claim format
        formatted_claims = []
        for msg in messages:
            # Support both schemas (messages and fact_checks)
            timestamp = msg.get("timestamp") or msg.get("created_at")
            transcript = msg.get("transcription") or msg.get("transcript", "")
            
            formatted_claims.append({
                "id": msg.get("id", "Unknown"),
                "claimSummary": msg.get("claim", "No summary"),
                "verdict": msg.get("verdict", "Unverified"),
                "language": msg.get("language", "English"),
                "confidence": int(msg.get("confidence", 0.9) * 100), # Default 90% if missing
                "viralityRisk": msg.get("virality_score", 0),
                "dateChecked": timestamp.isoformat() if hasattr(timestamp, 'isoformat') else str(timestamp),
                "originalTranscript": transcript,
                "translatedClaim": msg.get("claim", ""),
                "explanation": msg.get("explanation", "No explanation.")
            })
        return formatted_claims
    except Exception as e:
        logger.error(f"Error fetching claims for API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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



from services.storage_service import storage_service

async def handle_voice_message_pipeline(sender_id: str, media_id: str):
    """Downloads audio, uploads to Cloud Storage, and triggers the full AI pipeline."""
    try:
        await send_message(sender_id, "Voice note received! 🎤 analyzing...")
        # 1. Download audio file locally
        local_path = await download_media(media_id)
        if not local_path:
            logger.error(f"Could not download audio for media_id {media_id}")
            await send_message(sender_id, "I encountered an error while trying to download your voice note.")
            return

        # 2. Upload to Firebase Storage for permanent URL
        cloud_url = storage_service.upload_file(local_path, folder="voice_notes")
        logger.info(f"Audio uploaded to Cloud Storage: {cloud_url}")

        # 3. Trigger processing with cloud URL
        await background_process_audio_and_reply(sender_id, local_path, cloud_url)

    except Exception as e:
        logger.error(f"Error in voice pipeline: {str(e)}")
        await send_message(sender_id, "An unexpected error occurred while processing your request.")

async def background_process_audio_and_reply(sender_id: str, local_path: str, cloud_url: str):
    """Background task to run the AI pipeline for audio and send the result back via WhatsApp."""
    try:
        # 1. Whisper transcription ONLY (no LLM yet)
        logger.info("Running Whisper transcription for audio...")
        whisper_result = await asyncio.to_thread(transcribe_audio, local_path)
        text = whisper_result["text"]
        language = whisper_result.get("language", "English")

        print(f"\nDetected Language: {language}")
        print(f"Input transcription:\n{text}")

        # 2. Normalize transcript and check Firestore cache BEFORE any LLM call
        normalized = normalize_transcript(text)
        logger.info(f"Transcript normalized and checked against Firestore (audio pipeline).")
        cached = firebase_service.check_transcript_cache(normalized)
        if cached:
            await _send_cached_result(sender_id, text, cached)
            return

        logger.info("No transcript match – running full pipeline (audio).")

        # 3. Cache miss → extract claim with LLM
        lang_name = "English"
        extracted_claim = text  # fallback to raw text
        if settings.USE_LLM:
            logger.info("Extracting claim from audio transcription...")
            extractor = ClaimExtractor()
            extraction_result = extractor.extract_claim(text)
            if extraction_result:
                extracted_claim = extraction_result.get("claim") or text
                lang_name = extraction_result.get("language", "English")

        if not extracted_claim:
            await send_message(sender_id, "I couldn't extract a clear claim from your audio.")
            return

        # 4. Fact-check, store, and reply
        await handle_claim_verification(
            sender_id=sender_id,
            extracted_claim=extracted_claim,
            normalized_transcript=normalized,
            language=lang_name
        )

    except Exception as e:
        logger.error(f"Error processing audio in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the audio.")

async def background_process_image_and_reply(sender_id: str, media_id: str):
    """Background task to run the AI pipeline for images and send the result back via WhatsApp."""
    try:
        await send_message(sender_id, "Image received! 📸 extracting text...")
        
        # 1. Download media locally
        local_path = await download_media(media_id)
        if not local_path:
            await send_message(sender_id, "Sorry, I couldn't download the image.")
            return

        # 2. Upload to Firebase Storage for permanent URL
        cloud_url = storage_service.upload_file(local_path, folder="images")
        logger.info(f"Image uploaded to Cloud Storage: {cloud_url}")

        # 3. Extract text from image (OCR only, no LLM yet)
        logger.info(f"Running OCR on image: {local_path}")
        ocr_service = OCRService()
        extracted_text = ocr_service.extract_text(local_path)
        
        if not extracted_text:
            await send_message(sender_id, "I couldn't extract any text from the image.")
            return

        # 4. Normalize and check Firestore cache BEFORE any LLM call
        normalized = normalize_transcript(extracted_text)
        logger.info(f"Transcript normalized and checked against Firestore (image pipeline).")
        cached = firebase_service.check_transcript_cache(normalized)
        if cached:
            await _send_cached_result(sender_id, extracted_text, cached)
            return

        logger.info("No transcript match – running full pipeline (image).")

        # 5. Cache miss → extract claim with LLM
        logger.info(f"Extracting claim from OCR text...")
        extractor = ClaimExtractor()
        extraction_result = extractor.extract_claim(extracted_text)
        extracted_claim = extraction_result.get("claim")
        detected_language = extraction_result.get("language", "English")
        
        # 5. Fact-Check the claim
        engine = FactCheckerEngine()
        fact_check_result = engine.check_claim(extracted_claim, language=detected_language)

        time.sleep(3) # Mandatory pause for Free Tier stability
        await handle_claim_verification(
            sender_id=sender_id, 
            extracted_claim=extracted_claim, 
            full_text=extracted_text, 
            file_path=cloud_url, 
            media_type="image", 
            fact_check_result=fact_check_result,
        )


        
    except Exception as e:
        logger.error(f"Error processing image in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the image.")

async def background_process_text_and_reply(sender_id: str, text_content: str):
    """Background task to run the AI pipeline for plain text claims."""
    try:
        if not text_content:
            await send_message(sender_id, "Your message was empty. Please provide a claim to check.")
            return

        # 1. Normalize transcript and check Firestore cache BEFORE any LLM call
        normalized = normalize_transcript(text_content)
        logger.info(f"Transcript normalized and checked against Firestore (text pipeline).")
        cached = firebase_service.check_transcript_cache(normalized)
        if cached:
            await _send_cached_result(sender_id, text_content, cached)
            return

        logger.info("No transcript match – running full pipeline (text).")

        # 2. Cache miss → extract claim with LLM
        logger.info(f"Extracting claim from text...")
        extractor = ClaimExtractor()
        extraction_result = extractor.extract_claim(text_content)
        extracted_claim = extraction_result.get("claim")
        detected_language = extraction_result.get("language", "English")

        # 3. Fact-check and reply
        await handle_claim_verification(
            sender_id=sender_id,
            extracted_claim=extracted_claim,
            full_text=text_content,
            file_path=None,
            media_type="text",
            fact_check_result=fact_check_result,
            normalized_transcript=normalized,
            language=detected_language
        )
        
    except Exception as e:
        logger.error(f"Error processing text in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing your text claim.")

async def _send_cached_result(sender_id: str, original_text: str, cached: dict):
    """Formats and sends a cached fact-check result to the user over WhatsApp."""
    verdict = cached.get("verdict", "FALSE")
    
    # Use regional fields for display (WhatsApp)
    verdict_reg = cached.get("verdict_reg", verdict)
    explanation = cached.get("explanation_reg", cached.get("explanation_en", cached.get("explanation", "No explanation available.")))
    virality_score = cached.get("virality_score", 0)
    virality_reason = cached.get("virality_reason_reg", cached.get("virality_reason_en", cached.get("virality_reason", "")))
    counter_message = cached.get("counter_message_reg", cached.get("counter_message_en", cached.get("counter_message")))
    claim = cached.get("claim", original_text)
    language = cached.get("language", "English")

    reply_text = f"📢 Fact Check Result (Cached)\n\n"
    reply_text += f"Claim: {claim}\n\n"
    reply_text += f"Verdict: {verdict_reg}\n\n"
    reply_text += f"Explanation:\n{explanation}\n\n"
    reply_text += f"Virality Risk Score: {virality_score}/10\n\n"
    reply_text += f"Reason:\n{virality_reason}"
    if counter_message:
        reply_text += f"\n\nSuggested Counter Message:\n{counter_message}"

    await send_message(sender_id, reply_text)
    
    # Generate and Send Regional TTS Audio if not English
    if language and language.lower() not in ["english", "en"]:
        logger.info(f"Generating TTS for {language} output (from cache).")
        tts_text = f"Verdict: {verdict_reg}. Explanation: {explanation}"
        if counter_message:
            tts_text += f" Suggested response: {counter_message}"
            
        audio_path = await generate_regional_tts(tts_text)
        if audio_path:
            media_id = await upload_media(audio_path, mime_type="audio/mpeg")
            if media_id:
                await send_audio_message(sender_id, media_id)
            else:
                logger.error("Failed to upload TTS audio to WhatsApp.")
            
            # Optionally clean up the local audio file to save space
            try:
                os.remove(audio_path)
            except Exception as e:
                logger.warning(f"Could not remove temporary TTS audio file {audio_path}: {e}")

async def handle_claim_verification(sender_id, extracted_claim, normalized_transcript, language="English"):
    """
    Runs the fact-check pipeline and sends a WhatsApp reply.
    Called only on a cache MISS — normalization and Firestore cache check are done by the callers.
    """
    if not extracted_claim:
        await send_message(sender_id, "I couldn't extract a clear claim from your message.")
        return

    # Run the full fact-check pipeline
    engine = FactCheckerEngine()
    fact_check_result = engine.check_claim(extracted_claim, language=language)

    # Extract data from result structure
    verdict = fact_check_result.get("verdict", "FALSE")
    category = fact_check_result.get("category", "health")

    verdict_reg = fact_check_result.get("verdict_reg", verdict)
    explanation_disp = fact_check_result.get("explanation_reg", fact_check_result.get("explanation_en", "No explanation provided."))
    virality_score = fact_check_result.get("virality_score", 0)
    virality_reason_disp = fact_check_result.get("virality_reason_reg", fact_check_result.get("virality_reason_en", "No reason provided."))
    counter_message_disp = fact_check_result.get("counter_message_reg", fact_check_result.get("counter_message_en"))

    if fact_check_result.get("cached"):
        logger.info("Fact-check result served from semantic (vector) cache.")
    else:
        logger.info("Fact-check result generated via full pipeline.")

    header="🔎 Tattva AI Fact Check Result"
    # Always reply to user in their regional language
    reply_text = (
        f"📢 *Fact Check Result*\n\n"
        f"✅ *Verdict:* {verdict_reg}\n\n"
        f"📝 *Explanation:* {explanation_disp}"
    )
    if counter_message_disp:
        reply_text += f"\n\n📩 *Suggested Response:* {counter_message_disp}"
    
    # 3. Store in Firestore (English ONLY as per user request)
    message_data = MessageRecord(
        transcript=normalized_transcript,
        claim=extracted_claim,
        verdict=verdict,
        explanation=fact_check_result.get("explanation_en", explanation_disp),
        virality_score=virality_score,
        virality_reason=fact_check_result.get("virality_reason_en", virality_reason_disp),
        counter_message=fact_check_result.get("counter_message_en", counter_message_disp),
        language=language,
        category=category
    )
    firebase_service.save_message(message_data)

    # Send WhatsApp Text Reply
    await send_message(sender_id, reply_text)
    
    # Generate and Send Regional TTS Audio if not English
    if language and language.lower() not in ["english", "en"]:
        logger.info(f"Generating TTS for {language} output.")
        tts_text = f"Verdict: {verdict_reg}. Explanation: {explanation_disp}"
        if counter_message_disp:
            tts_text += f" Suggested response: {counter_message_disp}"
            
        audio_path = await generate_regional_tts(tts_text)
        if audio_path:
            media_id = await upload_media(audio_path, mime_type="audio/mpeg")
            if media_id:
                await send_audio_message(sender_id, media_id)
            else:
                logger.error("Failed to upload TTS audio to WhatsApp.")
            
            # Optionally clean up the local audio file to save space
            try:
                os.remove(audio_path)
            except Exception as e:
                logger.warning(f"Could not remove temporary TTS audio file {audio_path}: {e}")


async def process_audio(audio_path):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription")
    # 1. Transcribe audio (Run in thread to avoid blocking the event loop)
    whisper_result = await asyncio.to_thread(transcribe_audio, audio_path)
    
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
    fact_check_result = fact_checker.check_claim(claim, language=language_name)
    
    # 4. Handle verification (Internal mock for sender_id in CLI)
    # In CLI mode, we just print the result instead of sending WhatsApp
    verdict_reg = fact_check_result.get("verdict_reg", fact_check_result.get("verdict_en", "Unknown"))
    explanation_reg = fact_check_result.get("explanation_reg", fact_check_result.get("explanation_en", "No explanation provided."))
    counter_message_reg = fact_check_result.get("counter_message_reg", "Please verify facts.")

    print(f"\n--- Fact-Check Result ({language_name}) ---")
    print(f"Verdict: {verdict_reg}")
    print(f"Counter Message: {counter_message_reg}")
    print(f"Explanation: {explanation_reg}")
    print("-" * 40)
        
    return {
        "text": text,
        "language": language,
        "language_name": language_name,
        "claim": claim,
        "fact_check_result": fact_check_result
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
        
    import asyncio
    asyncio.run(process_audio(audio_file))
