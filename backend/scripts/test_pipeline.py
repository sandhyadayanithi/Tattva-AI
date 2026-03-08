import asyncio
import sys
import os
from pathlib import Path

# Add project root to python path to allow imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from main import background_process_text_and_reply

async def main():
    print("--- Starting Local Pipeline Test ---")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please add ELEVENLABS_API_KEY to your backend/.env to fully test TTS.")
        return
        
    print("Testing pipeline with a sample regional claim (Tamil)...")
    
    # A mock user WhatsApp number to send the results to (Replace with your actual number to see the result on WhatsApp!)
    # Format: CountryCode+PhoneNumber (e.g., "919876543210")
    test_sender_id = os.getenv("TEST_WHATSAPP_NUMBER", "1234567890") 
    
    # A fake health misinformation claim in Tamil
    test_claim = "சூடான எலுமிச்சை தண்ணீர் குடித்தால் எல்லா வகையான புற்றுநோயும் குணமாகும்."
    
    print(f"Mocking incoming WhatsApp message from user {test_sender_id}")
    print(f"Claim: {test_claim}")
    print("\nRunning background processing...")
    
    # Run the exact pipeline that the webhook runs
    await background_process_text_and_reply(
        sender_id=test_sender_id,
        text_content=test_claim
    )
    
    print("\n--- Pipeline Execution Finished ---")
    print("\nIf you used your real TEST_WHATSAPP_NUMBER, check your WhatsApp for the text reply and the generated voice note!")

if __name__ == "__main__":
    asyncio.run(main())
