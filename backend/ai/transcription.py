import whisper
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Resolve audio folder
AUDIO_DIR = BASE_DIR / "audio_files"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Whisper Model
_model = None

def _get_model():
    global _model
    if _model is None:
        logger.info("Loading Whisper model (base)...")
        # You can change the model size here: "tiny", "base", "small", "medium", "large"
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(filename):
    """
    Transcribes audio using local Whisper model.
    """
    audio_path = Path(filename)
    if not audio_path.is_absolute():
        # First try assuming it is relative to BASE_DIR (e.g., from command line)
        local_path = BASE_DIR / audio_path
        if local_path.exists():
            audio_path = local_path
        else:
            # Fallback to AUDIO_DIR for implicit names
            audio_path = AUDIO_DIR / audio_path.name

    logger.info(f"Attempting transcription via Whisper for: {audio_path}")

    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        return {"text": "", "language": "unknown", "error": f"File not found: {audio_path}"}

    try:
        model = _get_model()
        
        # Whisper transcribe
        result = model.transcribe(str(audio_path))
        
        text = result.get("text", "").strip()
        language = result.get("language", "unknown")

        logger.info(f"Whisper transcription successful ({language})")
        
        return {
            "text": text,
            "language": language,
        }
    except Exception as e:
        logger.error(f"Whisper transcription error: {str(e)}")
        return {
            "text": "",
            "language": "unknown",
            "error": f"Whisper Error: {str(e)}"
        }
