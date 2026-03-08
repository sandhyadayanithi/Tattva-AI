import sys
from pathlib import Path

# Add project root to python path to allow importing AI module
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from ai.transcription import transcribe_audio

def main():
    audio_file = "test_audio.mp3"
    print(f"Testing transcription on: {audio_file}")
    
    result = transcribe_audio(audio_file)
    print("\n--- Transcription Result ---")
    print(f"Language: {result.get('language')}")
    print(f"Text: {result.get('text')}")
    
    if "error" in result:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    main()
