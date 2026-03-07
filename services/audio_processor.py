import logging
from core.config import settings
from services.whatsapp import send_message
from services.whisper_service import transcribe_audio
from services.claim_extractor import ClaimExtractor
from services.fact_checker import FactCheckerEngine
import json

logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
USE_LLM = True
# ---------------------

async def background_process_audio_and_reply(sender_id: str, audio_path: str):
    """Background task to run the AI pipeline and send the result back via WhatsApp."""
    try:
        pipeline_result = process_audio(audio_path)
        extracted_claim = pipeline_result.get("claim")
        
        if extracted_claim:
            reply_text = f'Extracted Claim:\n"{extracted_claim}"\n\n(Fact check engine pending...)'
        else:
            reply_text = "I couldn't extract a clear claim from your audio."
            
        await send_message(sender_id, reply_text)
        
    except Exception as e:
        logger.error(f"Error processing audio in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the audio.")

def process_audio(audio_path):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription and language detection...")
    whisper_result = transcribe_audio(audio_path)
    
    text = whisper_result["text"]
    language = whisper_result["language"]
    
    print(f"\nDetected Language: {language}")
    print(f"Input transcription:\n{text}")
    
    claim = None
    fact_check_result = None
    
    if USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        claim = extractor.extract_claim(text)
        
        if claim:
            print(f"\nExtracted claim:\n{claim}")
            
            print("\n3. Running Fact Checker Engine...")
            fact_checker = FactCheckerEngine()
            fact_check_result = fact_checker.check_claim(claim)
            
            # Print the result to terminal without evidence
            output_result = {k: v for k, v in fact_check_result.items() if k != "evidence_used"}
            print(json.dumps(output_result, indent=2))
            print("\n" + "-"*40 + "\n")
            
        else:
            print("\nFailed to extract claim.")
    else:
        print("\n2. [SKIPPED] LLM Claim Extraction disabled by USE_LLM flag.")
        
    return {
        "text": text,
        "language": language,
        "claim": claim,
        "fact_check_result": fact_check_result
    }
