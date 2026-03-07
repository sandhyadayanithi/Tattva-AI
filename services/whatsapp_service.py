import httpx
import logging
import asyncio
from pathlib import Path
from core.config import settings

logger = logging.getLogger(__name__)

# WhatsApp API base
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER_ID}"

# HTTP timeout
DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# Resolve project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder where downloaded media will be stored
AUDIO_DIR = BASE_DIR / "audio_files"
MEDIA_DIR = BASE_DIR / "media_files"

# Ensure the directories exist
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


async def _request_with_retry(method: str, url: str, **kwargs):
    """Internal helper to handle httpx requests with retries."""
    max_retries = 3

    for attempt in range(max_retries):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            try:
                if method.upper() == "POST":
                    response = await client.post(url, **kwargs)
                else:
                    response = await client.get(url, **kwargs)

                response.raise_for_status()

                if response.content:
                    return response.json()
                return None

            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.warning(
                    f"Timeout on attempt {attempt + 1}/{max_retries} for {url}: {str(e)}"
                )

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP {e.response.status_code} for {url} on attempt {attempt + 1}: {e.response.text}"
                )

                # Don't retry most 4xx errors
                if e.response.status_code < 500 and e.response.status_code != 429:
                    break

            except Exception as e:
                logger.error(
                    f"Unexpected error on attempt {attempt + 1} for {url}: {str(e)}"
                )

        if attempt < max_retries - 1:
            await asyncio.sleep(1 * (attempt + 1))

    return None


async def send_message(to: str, text: str):
    """Send a WhatsApp text message."""
    url = f"{WHATSAPP_API_URL}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    result = await _request_with_retry("POST", url, headers=headers, json=payload)

    if result:
        logger.info(f"Message sent successfully to {to}")

    return result


async def mark_as_read(message_id: str):
    """Mark an incoming WhatsApp message as read."""
    url = f"{WHATSAPP_API_URL}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }

    result = await _request_with_retry("POST", url, headers=headers, json=payload)

    if result:
        logger.info(f"Message {message_id} marked as read")
    else:
        logger.warning(f"Failed to mark message {message_id} as read after retries.")

    return result

async def download_media(media_id: str) -> str:
    """
    Download WhatsApp media given a media_id.
    Returns the absolute file path of the saved file.
    """

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
    }

    metadata_url = f"https://graph.facebook.com/v18.0/{media_id}"

    media_data = await _request_with_retry("GET", metadata_url, headers=headers)

    if not media_data or not media_data.get("url"):
        logger.error(f"Could not retrieve media metadata for {media_id}")
        return None

    media_url = media_data["url"]
    mime_type = media_data.get("mime_type", "")

    # Determine extension
    ext = ".bin"
    if "audio/ogg" in mime_type or "audio/opus" in mime_type:
        ext = ".ogg"
    elif "image/jpeg" in mime_type:
        ext = ".jpg"
    elif "image/png" in mime_type:
        ext = ".png"
    elif "video/mp4" in mime_type:
        ext = ".mp4"

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            response = await client.get(media_url, headers=headers)
            response.raise_for_status()

            file_path = AUDIO_DIR / f"{media_id}{ext}"

            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Media downloaded successfully to: {file_path}")

            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to download binary from {media_url}: {str(e)}")
            return None