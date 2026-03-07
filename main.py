import sys
import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, Request, HTTPException, Response, BackgroundTasks
import logging
from core.config import settings
from services.whatsapp import download_media, send_message
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
    Incoming webhook for WhatsApp messages.
    """
    body = await request.json()
    logger.info(f"Incoming webhook: {body}")
    
    # Expected Meta structure parsing
    try:
        # Check if it's a message event
        if "object" in body and body["object"] == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for changes in entry.get("changes", []):
                    value = changes.get("value", {})
                    # Ensure it's a message, not a status update
                    if "messages" in value:
                        for message in value["messages"]:
                            sender_id = message.get("from")
                            
                            if message.get("type") == "audio":
                                audio = message.get("audio", {})
                                media_id = audio.get("id")
                                
                                logger.info(f"Received audio message from {sender_id}. Media ID: {media_id}")
                                
                                # Send acknowledgment
                                await send_message(sender_id, "Audio received. Processing...")
                                
                                # Download media
                                file_path = await download_media(media_id)
                                
                                if file_path:
                                    logger.info(f"Audio downloaded to: {file_path}")
                                    # Process audio in the background to avoid Meta webhook timeout (which is ~15s)
                                    background_tasks.add_task(background_process_audio_and_reply, sender_id, file_path)
                                else:
                                    await send_message(sender_id, "Sorry, I couldn't download the audio.")
                            else:
                                logger.info(f"Received non-audio message from {sender_id}")
                                await send_message(sender_id, "Please send a voice note to check a claim.")
                                
        return Response(content="EVENT_RECEIVED", status_code=200)

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response(content="ERROR", status_code=500)

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
    result = vector_service.store_claim(claim, verdict, explanation)
    return {"id": result, "status": "stored"}



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
        engine = FactCheckerEngine()
        fact_check_result = engine.check_claim(extracted_claim)
        
        verdict = fact_check_result.get("verdict", "Unknown")
        explanation = fact_check_result.get("explanation", "No explanation provided.")
        confidence = fact_check_result.get("confidence_level", "Low")
        
        if fact_check_result.get("cached"):
            logger.info("Found similar claim in cache.")
            reply_text = f"🔍 *Found a Similar Cached Claim*\n\nClaim: {fact_check_result.get('claim', extracted_claim)}\n\n*Verdict:* {verdict}\n\n_Explanation:_ {explanation}"
        else:
            reply_text = f"✅ *Fact-Checked Result*\n\nClaim: {extracted_claim}\n\n*Verdict:* {verdict}\n\n_Explanation:_ {explanation}"
        
        # 3. Store in Firestore (FirebaseService)
        message_data = MessageRecord(
            user_number=sender_id,
            audio_file=audio_path,
            transcription=transcription,
            claim=extracted_claim,
            verdict=verdict,
            explanation=explanation,
            confidence=0.9 if confidence == "High" else 0.5 # Mapping scale
        )
        firebase_service.save_message(message_data)

        
        # 4. If new claim and was fact-checked (not needed now for placeholder), 
        # normally we'd do: vector_service.store_claim_embedding(extracted_claim, verdict, explanation)

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
    
    claim = None
    if USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        claim = extractor.extract_claim(text)
        
        if claim:
            print(f"\nExtracted claim:\n{claim}")
        else:
            print("\nFailed to extract claim.")
    else:
        print("\n2. [SKIPPED] LLM Claim Extraction disabled by USE_LLM flag.")
        
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
