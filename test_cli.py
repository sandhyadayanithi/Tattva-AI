import sys
import os
import json
import asyncio
from main import process_audio, handle_claim_verification
from services.ocr_service import OCRService
from ai.claim_extractor import ClaimExtractor
import logging

# Setup basic logging
logging.basicConfig(level=logging.ERROR) # Lower noise
logger = logging.getLogger("TestCLI")

def check_env():
    print("--- Environment Diagnostic ---")
    gemini_key = os.getenv("GEMINI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if not gemini_key:
        print("[FAIL] GEMINI_API_KEY is missing in .env")
    elif not gemini_key.startswith("AIza"):
        print("[WARN] GEMINI_API_KEY format looks unusual.")
    else:
        print("[OK] GEMINI_API_KEY detected.")

    if not tavily_key:
        print("[FAIL] TAVILY_API_KEY is missing in .env")
    elif not tavily_key.startswith("tvly-"):
        print("[FAIL] TAVILY_API_KEY format is INVALID. It should start with 'tvly-'.")
        print("       It looks like you might have accidentally pasted a Google/Gemini key here.")
    else:
        print("[OK] TAVILY_API_KEY detected.")
    print("-----------------------------\n")

async def test_image(image_path):
    check_env()
    print(f"\n[TEST] Processing Image: {image_path}")
    
    # 1. OCR
    from services.ocr_service import OCRService
    ocr_service = OCRService()
    extracted_text = ocr_service.extract_text(image_path)
    print(f"Extracted Text: {extracted_text[:100]}...")
    
    # 2. Mock processing
    await run_pipeline_and_print("test_user_image", extracted_text, image_path, "image")

def test_audio(audio_path):
    check_env()
    print(f"\n[TEST] Processing Audio: {audio_path}")
    
    # 1. Transcribe
    from ai.transcription import transcribe_audio
    result = transcribe_audio(audio_path)
    text = result["text"]
    print(f"Transcription: {text[:100]}...")
    
    # 2. Mock processing
    asyncio.run(run_pipeline_and_print("test_user_audio", text, audio_path, "audio"))

async def test_text(text_content):
    check_env()
    print(f"\n[TEST] Processing Text: {text_content[:100]}...")
    
    # 1. Mock processing
    await run_pipeline_and_print("test_user_text", text_content, None, "text")

async def run_pipeline_and_print(user_id, text, file_path, media_type):
    from ai.claim_extractor import ClaimExtractor
    from ai.fact_checker import FactCheckerEngine
    from main import handle_claim_verification
    import main
    
    print(f"Extracting claim...")
    extractor = ClaimExtractor()
    claim = extractor.extract_claim(text)
    print(f"Claim: {claim}")
    
    original_send = main.send_message
    
    async def mock_send(recipient_id, message):
        pass
    
    main.send_message = mock_send
    
    engine = FactCheckerEngine()
    result = engine.check_claim(claim)
    
    print("\n--- FINAL JSON OUTPUT ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-----------------------------\n")
    
    # Still call storage logic
    try:
        await handle_claim_verification(user_id, claim, text, file_path, media_type)
    except Exception as e:
        # Silencing Expected Firebase Initialization Errors in CLI
        pass
        
    main.send_message = original_send

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_cli.py <mode> <input>")
        print("Modes: image, audio, text")
        sys.exit(1)
        
    mode = sys.argv[1].lower()
    input_val = sys.argv[2]
    
    if mode == "image":
        if not os.path.exists(input_val):
             print(f"Error: File not found: {input_val}")
             sys.exit(1)
        asyncio.run(test_image(input_val))
    elif mode == "audio":
        if not os.path.exists(input_val):
             print(f"Error: File not found: {input_val}")
             sys.exit(1)
        test_audio(input_val)
    elif mode == "text":
        asyncio.run(test_text(input_val))
    else:
        print(f"Unknown mode: {mode}")
