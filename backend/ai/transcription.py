import google.generativeai as genai
import os
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Resolve audio folder
AUDIO_DIR = BASE_DIR / "audio_files"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Gemini Model
_model = None

def _get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-2.5-flash")
    return _model

def transcribe_audio(filename):
    """
    Transcribes audio using Gemini's API.
    Bypasses the need for local Whisper/FFmpeg dependencies.
    """
    audio_path = Path(filename)
    if not audio_path.is_absolute():
        audio_path = AUDIO_DIR / audio_path

    logger.info(f"Attempting transcription via Gemini for: {audio_path}")

    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        return {"text": "", "language": "unknown", "error": "File not found"}

    try:
        model = _get_model()
        
        # Determine mime type based on extension
        mime_type = "audio/ogg" if audio_path.suffix == ".ogg" else "audio/mpeg"
        
        # Prepare the parts
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        prompt = (
            "You are a professional transcription assistant. "
            "Transcribe the following audio file exactly. "
            "Detect the original language and return the results in the following JSON format:\n"
            "{\n"
            "  \"text\": \"The transcription here\",\n"
            "  \"language\": \"The name of the detected language\"\n"
            "}"
        )

        response = model.generate_content([
            prompt,
            {"mime_type": mime_type, "data": audio_data}
        ])
        
        content = response.text.strip()
        
        # Simple cleanup
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        import json
        try:
            result = json.loads(content)
            text = result.get("text", "").strip()
            language = result.get("language", "English").strip()
        except:
            # Fallback if JSON fails
            text = content
            language = "English"

        logger.info(f"Gemini transcription successful ({language})")
        
        return {
            "text": text,
            "language": language,
        }
    except Exception as e:
        logger.error(f"Gemini transcription error: {str(e)}")
        # Provide a descriptive error message if missing FFmpeg is still a potential concern
        # (Though with Gemini, we don't need it)
        return {
            "text": "",
            "language": "unknown",
            "error": f"API Error: {str(e)}"
        }
