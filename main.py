import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from whisper_service import transcribe_audio
from claim_extractor import ClaimExtractor

# --- CONFIGURATION ---
# Set this to False if you only want to test Whisper and save Gemini API calls
USE_LLM = True
# ---------------------

def process_audio(audio_path):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription and language detection...")
    whisper_result = transcribe_audio(audio_path)
    
    text = whisper_result["text"]
    language = whisper_result["language"]
    
    print(f"\nDetected Language: {language}")
    print(f"Input transcription:\n{text}")
    
    claim = None
    if USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        claim = extractor.extract_claim(text)
        
        if claim:
            print(f"\nExtracted claim:\n{claim}")
        else:
            print("\nFailed to extract claim.")
    else:
        print("\n2. [SKIPPED] LLM Claim Extraction disabled by USE_LLM flag.")
        
    return {
        "text": text,
        "language": language,
        "claim": claim
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)
        
    process_audio(audio_file)
