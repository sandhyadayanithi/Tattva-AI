# check_firebase_v2.py
from config.firebase_config import db
import json

def check_all_fields():
    print("--- FETCHING LATEST MESSAGE FROM FIRESTORE ---")
    docs = db.collection("messages").order_by("timestamp", direction="DESCENDING").limit(1).stream()
    
    found = False
    for doc in docs:
        found = True
        data = doc.to_dict()
        print(f"Document ID:   {doc.id}")
        print(f"1. Audio File:    {data.get('audio_file')}")
        print(f"2. Transcription: {data.get('transcription')}")
        print(f"3. Claim:         {data.get('claim')}")
        print(f"4. Verdict:       {data.get('verdict')}")
        print(f"5. Explanation:   {data.get('explanation')}")
        print(f"6. Counter Msg:   {data.get('counter_message')}")
        print(f"7. Confidence:    {data.get('confidence')}")
        print(f"8. Timestamp:     {data.get('timestamp')}")
        print("-" * 50)
        
        # Also print the raw keys to be 100% sure
        print(f"Raw Keys present: {list(data.keys())}")
    
    if not found:
        print("No messages found.")

if __name__ == "__main__":
    check_all_fields()
