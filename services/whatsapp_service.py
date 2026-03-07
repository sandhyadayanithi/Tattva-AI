import httpx
import os
import logging
import asyncio
from core.config import settings

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER_ID}"
DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)

async def _request_with_retry(method: str, url: str, **kwargs):
    """Internal helper to handle httpx requests with retries and logging."""
    max_retries = 3
    for attempt in range(max_retries):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            try:
                if method.upper() == "POST":
                    response = await client.post(url, **kwargs)
                else:
                    response = await client.get(url, **kwargs)
                
                response.raise_for_status()
                return response.json()
            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries} for {url}: {str(e)}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP {e.response.status_code} for {url} on attempt {attempt + 1}: {e.response.text}")
                # Don't retry on 4xx errors except maybe 429
                if e.response.status_code < 500 and e.response.status_code != 429:
                    break
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1} for {url}: {str(e)}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(1 * (attempt + 1)) # Simple backoff
            
    return None

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
    
    result = await _request_with_retry("POST", url, headers=headers, json=payload)
    if result:
        logger.info(f"Message sent successfully to {to}")
    return result

async def mark_as_read(message_id: str):
    """Marks an incoming message as read using the official Meta format."""
    url = f"{WHATSAPP_API_URL}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    # Official payload structure for status updates
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }

    result = await _request_with_retry("POST", url, headers=headers, json=payload)
    if result:
        logger.info(f"Message {message_id} marked as read")
    else:
        logger.warning(f"Failed to mark message {message_id} as read after retries.")
    return result

async def download_media(media_id: str, folder="media") -> str:
    """Downloads media from WhatsApp and returns the local file path."""
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}

    async with httpx.AsyncClient() as client:
        try:
            # 1. Get the media URL and metadata
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            media_data = response.json()
            media_url = media_data.get("url")
            mime_type = media_data.get("mime_type", "")
            
            if not media_url:
                logger.error(f"No media URL found for {media_id}")
                return None
            
            # Determine extension from MIME type
            ext = ".bin"
            if "audio/ogg" in mime_type or "audio/opus" in mime_type: ext = ".ogg"
            elif "image/jpeg" in mime_type: ext = ".jpg"
            elif "image/png" in mime_type: ext = ".png"
            elif "video/mp4" in mime_type: ext = ".mp4"
            
            # 2. Download the actual media file
            media_response = await client.get(media_url, headers=headers)
            media_response.raise_for_status()
            
            # 3. Save it locally
            os.makedirs(folder, exist_ok=True)
            file_path = f"{folder}/{media_id}{ext}"
            with open(file_path, "wb") as f:
                f.write(media_response.content)
            
            logger.info(f"Successfully downloaded {mime_type} to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Media download failed: {str(e)}")
            return None
