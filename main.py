import sys
import os
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

# --- CONFIGURATION ---
# Set this to False if you only want to test Whisper and save Gemini API calls
USE_LLM = True
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
    Incoming webhook for WhatsApp messages from Meta API.
    """
    try:
        body = await request.json()
        logger.info(f"Incoming WhatsApp webhook: {json.dumps(body)}")
        
        # Meta sends a list of changes
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            sender_id = message.get("from")
                            message_id = message.get("id")
                            
                            # Mark message as read
                            background_tasks.add_task(mark_as_read, message_id)
                            
                            if message.get("type") == "audio":
                                audio = message.get("audio", {})
                                media_id = audio.get("id")
                                
                                logger.info(f"Received audio from {sender_id}. Media ID: {media_id}")
                                
                                # Send acknowledgment
                                await send_message(sender_id, "Voice note received! 🎤 I'm analyzing the claim. Please wait a moment...")
                                
                                # Process audio in background
                                background_tasks.add_task(handle_voice_message_pipeline, sender_id, media_id)
                            else:
                                logger.info(f"Received non-audio message from {sender_id}")
                                await send_message(sender_id, "Please send a voice note (audio message) to verify a claim.")
                                
        return Response(content="EVENT_RECEIVED", status_code=200)

    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        return Response(content="ERROR", status_code=200) # Always return 200 to Meta to avoid retries on processing errors

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
    """Background task to run the AI pipeline and send the result back via WhatsApp."""
    try:
        # 1. Run Pipeline (Whisper + Claim Extractor)
        pipeline_result = process_audio(audio_path)
        extracted_claim = pipeline_result.get("claim")
        transcription = pipeline_result.get("text")
        
        if not extracted_claim:
            await send_message(sender_id, "I couldn't extract a clear claim from your audio.")
            return

        # 2. Fact-Check the claim (Checks Vector Cache internally)
        engine = FactCheckerEngine(use_llm=USE_LLM)
        fact_check_result = engine.check_claim(extracted_claim)
        
        verdict = fact_check_result.get("verdict", "Unknown")
        explanation = fact_check_result.get("explanation", "No explanation provided.")
        confidence = fact_check_result.get("confidence_level", "Low")
        
        if fact_check_result.get("cached"):
            logger.info("Found similar claim in cache.")
            reply_text = (
                f"🔍 *Previous Fact-Check Found*\n\n"
                f"*Claim Detected:* \"{fact_check_result.get('claim', extracted_claim)}\"\n\n"
                f"*Verdict:* {verdict}\n\n"
                f"*Explanation:* {explanation}"
            )
        else:
            reply_text = (
                f"✅ *Fact-Check Complete*\n\n"
                f"*Claim Detected:* \"{extracted_claim}\"\n\n"
                f"*Verdict:* {verdict}\n\n"
                f"*Explanation:* {explanation}"
            )
        
        # 3. Store in Firestore (FirebaseService)
        message_data = MessageRecord(
            user_number=sender_id,
            audio_file=audio_path,
            transcription=transcription,
            claim=extracted_claim,
            verdict=verdict,
            explanation=explanation,
            confidence=0.9 if confidence == "High" else 0.5, # Mapping scale
            raw_fact_check_response=fact_check_result
        )
        firebase_service.save_message(message_data)

        # 4. Send the final response
        await send_message(sender_id, reply_text)
        
    except Exception as e:
        logger.error(f"Error processing audio in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the audio.")


def process_audio(audio_path):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription and language detection...")
    whisper_result = transcribe_audio(audio_path)
    
    text = whisper_result["text"]
    language = whisper_result["language"]
    
    print(f"\nDetected Language: {language}")
    print(f"Input transcription:\n{text}")
    
    claim = text  # Default to raw text
    if USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        extracted = extractor.extract_claim(text)
        if extracted:
            claim = extracted
            print(f"\nExtracted claim:\n{claim}")
        else:
            print("\nFailed to extract claim.")
    else:
        print("\n2. [SKIPPED] Claim Extraction disabled. Using raw transcription as claim.")

    print("\n3. Running Fact Checker Engine...")
    fact_checker = FactCheckerEngine(use_llm=USE_LLM)
    # This searches Tavily and optionally runs Gemini for the verdict.
    result = fact_checker.check_claim(claim)
    
    # Print the terminal output (filtering out the large body of evidence)
    output_result = {k: v for k, v in result.items() if k != "evidence_used"}
    print(json.dumps(output_result, indent=2))
    print("\n" + "-"*40 + "\n")
        
    return {
        "text": text,
        "language": language,
        "claim": claim
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)
        
    process_audio(audio_file)
