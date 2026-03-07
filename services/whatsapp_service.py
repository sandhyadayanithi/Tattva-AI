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

async def download_media(media_id: str) -> str:
    """Downloads media from WhatsApp given a media_id and returns the absolute local file path."""
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
    }

    # 1. Get the media URL
    media_data = await _request_with_retry("GET", url, headers=headers)
    if not media_data or not media_data.get("url"):
        logger.error(f"Could not retrieve media metadata for {media_id}")
        return None
        
    media_url = media_data.get("url")
    
    # 2. Download the actual media file
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            # Note: For media downloads, we still use the token as Meta recommends
            response = await client.get(media_url, headers=headers)
            response.raise_for_status()
            
            # 3. Save it locally using absolute path
            mime_type = media_data.get("mime_type", "")
            ext = ".ogg" if "audio" in mime_type else ".jpg" if "image" in mime_type else ".bin"
            
            file_path = AUDIO_DIR / f"{media_id}{ext}"
            
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"Successfully downloaded media to: {file_path.absolute()}")
            return str(file_path.absolute())
        except Exception as e:
            logger.error(f"Failed to download binary from {media_url}: {str(e)}")
            return None
