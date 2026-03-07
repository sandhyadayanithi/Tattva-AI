import logging
from core.config import settings
from services.whatsapp import send_message
from ai.transcription import transcribe_audio
from ai.claim_extractor import ClaimExtractor
from ai.fact_checker import FactCheckerEngine
from services.firebase_service import firebase_service
from models.message_model import MessageRecord
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# --- CONFIGURATION (Global settings in core.config) ---
# ---------------------

async def background_process_audio_and_reply(sender_id: str, audio_path: str):
    """Background task to run the AI pipeline and send the result back via WhatsApp."""
    try:
        # Use our centralized process_audio function
        pipeline_result = process_audio(audio_path, user_number=sender_id)
        
        extracted_claim = pipeline_result.get("claim")
        transcription = pipeline_result.get("text")
        fact_check_result = pipeline_result.get("fact_check_result")

        if not extracted_claim:
            await send_message(sender_id, "I couldn't extract a clear claim from your audio.")
            return

        verdict = fact_check_result.get("verdict", "Unknown")
        explanation = fact_check_result.get("explanation", "No explanation provided.")
        
        if fact_check_result.get("cached"):
            reply_text = f"🔍 *Found a Similar Cached Claim*\n\nClaim: {fact_check_result.get('claim', extracted_claim)}\n\n*Verdict:* {verdict}\n\n_Explanation:_ {explanation}"
        else:
            reply_text = f"✅ *Fact-Checked Result*\n\nClaim: {extracted_claim}\n\n*Verdict:* {verdict}\n\n_Explanation:_ {explanation}"
            
        await send_message(sender_id, reply_text)
        
    except Exception as e:
        logger.error(f"Error processing audio in background: {e}")
        await send_message(sender_id, "An error occurred while analyzing the audio.")

def process_audio(audio_path, user_number="TERMINAL_USER"):
    print(f"Processing audio file: {audio_path}")
    print("1. Running Whisper for transcription and language detection...")
    whisper_result = transcribe_audio(audio_path)
    
    text = whisper_result["text"]
    language = whisper_result["language"]
    
    print(f"\nDetected Language: {language}")
    print(f"Input transcription:\n{text}")
    
    claim = text # Default to raw text if no LLM
    fact_check_result = None
    
    if settings.USE_LLM:
        print("\n2. Extracting claims with LLM...")
        extractor = ClaimExtractor()
        extracted = extractor.extract_claim(text)
        if extracted:
            claim = extracted
            print(f"\nExtracted claim:\n{claim}")
    else:
        print("\n2. [SKIPPED] Claim extraction disabled. Using raw transcription.")

    print("\n3. Running Fact Checker Engine...")
    fact_checker = FactCheckerEngine(use_llm=settings.USE_LLM)
    fact_check_result = fact_checker.check_claim(claim)
    
    # Print the result to terminal without evidence
    output_result = {k: v for k, v in fact_check_result.items() if k != "evidence_used"}
    print(json.dumps(output_result, indent=2))
    
    # 4. STORE IN FIREBASE (Unifies terminal and webhook paths!)
    try:
        # Extract results with robust fallbacks
        verdict = fact_check_result.get("verdict", "Unknown")
        explanation = fact_check_result.get("explanation", "")
        counter = fact_check_result.get("counter_message") or fact_check_result.get("counter-message") or ""
        
        # Handle confidence mapping (Gemini might return confidence_score or confidence_level)
        conf = fact_check_result.get("confidence_score")
        if conf is None:
            # Fallback for old cache or different LLM formats
            level = fact_check_result.get("confidence_level", "").lower()
            if "high" in level: conf = 0.9
            elif "medium" in level: conf = 0.7
            elif "low" in level: conf = 0.4
            else: conf = 0.0

        message_record = MessageRecord(
            audio_file=os.path.basename(audio_path),
            transcription=text,
            claim=claim,
            verdict=verdict,
            explanation=explanation,
            counter_message=counter,
            confidence=float(conf),
        )
        firebase_service.save_message(message_record)
    except Exception as e:
        print(f"Warning: Failed to log result in Firebase: {e}")

    print("\n" + "-"*40 + "\n")
        
    return {
        "text": text,
        "language": language,
        "claim": claim,
        "fact_check_result": fact_check_result
    }
