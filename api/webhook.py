import logging
from fastapi import APIRouter, Request, HTTPException, Response, BackgroundTasks
from core.config import settings
from services.whatsapp_service import download_media, send_message
from services.audio_processor import background_process_audio_and_reply

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/webhook")
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

@router.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Incoming webhook for WhatsApp messages.
    """
    body = await request.json()
    logger.info(f"Incoming webhook: {body}")
    
    try:
        if "object" in body and body["object"] == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for changes in entry.get("changes", []):
                    value = changes.get("value", {})
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
                                    # Process audio in the background to avoid Meta webhook timeout (~15s)
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
