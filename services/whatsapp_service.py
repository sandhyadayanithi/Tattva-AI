import httpx
import os
import logging
from core.config import settings

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER_ID}"

async def send_message(to: str, text: str):
    """Sends a text message to a WhatsApp number."""
    url = f"{WHATSAPP_API_URL}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {to}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to send message: {e.response.text}")
            return None

async def mark_as_read(message_id: str):
    """Marks an incoming message as read."""
    url = f"{WHATSAPP_API_URL}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"Message {message_id} marked as read")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to mark message as read: {e.response.text}")
            return None

async def download_media(media_id: str) -> str:
    """Downloads media from WhatsApp given a media_id and returns the local file path."""
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        try:
            # 1. Get the media URL from WhatsApp API
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            media_data = response.json()
            media_url = media_data.get("url")
            
            if not media_url:
                logger.error(f"No media URL found in response for media_id {media_id}")
                return None
            
            # 2. Download the actual media file
            # Meta recommends not sending the Authorization header when requesting the media_url, 
            # but usually it's required for the initial URL fetch.
            media_response = await client.get(media_url, headers=headers)
            media_response.raise_for_status()
            
            # 3. Save it locally
            os.makedirs("audio_files", exist_ok=True)
            # WhatsApp voice notes are usually .ogg (Opus)
            file_path = f"audio_files/{media_id}.ogg"
            with open(file_path, "wb") as f:
                f.write(media_response.content)
            
            logger.info(f"Successfully downloaded audio to {file_path}")
            return file_path
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to download media: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during media download: {str(e)}")
            return None
