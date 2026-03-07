import whisper
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Audio directory
AUDIO_DIR = BASE_DIR / "audio_files"
AUDIO_DIR.mkdir(exist_ok=True)

# Load Whisper model (base is lightweight for hackathons)
_model = None

def transcribe_audio(filename):
    """
    Initializes and runs Whisper speech-to-text on an audio file.
    Expects a filename (or relative path from audio_files/) and uses absolute path for Whisper.
    """
    global _model
    
    # Construct absolute path
    audio_path = AUDIO_DIR / filename
    
    logger.info(f"Attempting transcription for: {audio_path}")

    if not audio_path.exists():
        logger.error(f"Audio file not found at absolute path: {audio_path}")
        return {
            "text": "",
            "language": "unknown",
            "error": "File not found"
        }

    if _model is None:
        logger.info("Loading Whisper model (base)...")
        _model = whisper.load_model("base")
    
    try:
        # Pass the absolute path string to Whisper
        result = _model.transcribe(str(audio_path))
        logger.info("Transcription successful")
        return {
            "text": result["text"].strip(),
            "language": result.get("language", "unknown")
        }
    except Exception as e:
        logger.error(f"Whisper transcription error: {str(e)}")
        return {
            "text": "",
            "language": "unknown",
            "error": str(e)
        }
