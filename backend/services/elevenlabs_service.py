import os
import httpx
import logging
from pathlib import Path
from core.config import settings

logger = logging.getLogger(__name__)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Resolve audio folder
AUDIO_DIR = BASE_DIR / "audio_files"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

async def generate_regional_tts(text: str) -> str:
    """
    Generate Text-to-Speech using ElevenLabs for the given text.
    Uses the multilingual model suitable for Indian regional languages.
    Returns the absolute path to the generated MP3 file.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        logger.error("ELEVENLABS_API_KEY is not set in environment variables.")
        return None

    # Using Rachel voice ID as deafult (or any multilingual voice ID we have selected)
    # 21m00Tcm4TlvDq8ikWAM is Rachel, you can replace with a preferred voice ID
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            # Generate a unique filename based on hash or timestamp
            import time
            timestamp = int(time.time() * 1000)
            file_path = AUDIO_DIR / f"tts_{timestamp}.mp3"
            
            with open(file_path, "wb") as f:
                f.write(response.content)
                
            logger.info(f"ElevenLabs TTS generated successfully: {file_path}")
            return str(file_path)
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during ElevenLabs TTS generation: {e}")
        if hasattr(e, "response") and e.response:
            logger.error(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during ElevenLabs TTS generation: {e}")
        return None
