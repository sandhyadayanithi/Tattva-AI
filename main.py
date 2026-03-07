import sys
import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, Request, HTTPException, Response, BackgroundTasks
import logging
from core.config import settings
from services.whatsapp import download_media, send_message
from whisper_service import transcribe_audio
from claim_extractor import ClaimExtractor

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

async def background_process_audio_and_reply(sender_id: str, audio_path: str):
    """Background task to run the AI pipeline and send the result back via WhatsApp."""
    try:
        pipeline_result = process_audio(audio_path)
        extracted_claim = pipeline_result.get("claim")
        
        if extracted_claim:
            # Person 3 will add fact_checker here. For now, we return the claim.
            reply_text = f'Extracted Claim:\n"{extracted_claim}"\n\n(Fact check engine pending...)'
        else:
            reply_text = "I couldn't extract a clear claim from your audio."
            
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
    print("\n2. Extracting claims with LLM...")
    
    extractor = ClaimExtractor()
    claim = extractor.extract_claim(text)
    
    if claim:
        print(f"\nExtracted claim:\n{claim}")
    else:
        print("\nFailed to extract claim.")
        
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
