import os
from services.audio_processor import process_audio
import json

def debug_process():
    audio_path = "audio_files/test_audio.mp3"
    print(f"DEBUG: Processing {audio_path}")
    result = process_audio(audio_path)
    
    print("\n--- DEBUG: fact_checker_result KEYS ---")
    fcr = result.get("fact_check_result", {})
    print(f"Keys: {list(fcr.keys())}")
    print(f"Confidence Score Key value: {fcr.get('confidence_score')}")
    print(f"Score Key value (if exists): {fcr.get('score')}")
    print("\n--- FULL RESULT ---")
    print(json.dumps(fcr, indent=2, default=str))

if __name__ == "__main__":
    debug_process()
