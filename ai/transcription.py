import whisper
from utils.logger import logger

# Load Whisper model (base is lightweight for hackathons)
_model = None

def transcribe_audio(audio_path):
    """Initializes and runs Whisper speech-to-text on an audio file."""
    global _model
    if _model is None:
        logger.info("Loading Whisper model (base)...")
        _model = whisper.load_model("base")
    
    logger.info(f"Transcribing audio file: {audio_path}")
    result = _model.transcribe(audio_path)
    return {
        "text": result["text"].strip(),
        "language": result.get("language", "unknown")
    }
