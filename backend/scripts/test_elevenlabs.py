import asyncio
import sys
import os
from pathlib import Path

# Add project root to python path to allow imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from services.elevenlabs_service import generate_regional_tts

async def main():
    print("Testing ElevenLabs TTS generation...")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("Please add ELEVENLABS_API_KEY to your backend/.env to run this test.")
        return
        
    test_text = "வணக்கம், இது பரிசோதனைக்கான குரல். Verdict: உண்மை."
    
    result_path = await generate_regional_tts(test_text)
    
    if result_path and os.path.exists(result_path):
        print(f"✅ Success! Audio file saved to: {result_path}")
    else:
        print("❌ Failed to generate audio.")

if __name__ == "__main__":
    asyncio.run(main())
