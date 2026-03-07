# test_storage_isolated.py
import os
import sys
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.getcwd())

from models.message_model import MessageRecord
from services.firebase_service import firebase_service

def test_storage():
    print("--- Running Isolated Storage Test ---")
    
    # Create a dummy message record with the counter_message field
    test_record = MessageRecord(
        audio_file="isolated_test.ogg",
        transcription="This is a test transcription.",
        claim="Test Claim",
        verdict="True",
        explanation="Test Explanation about the verdict.",
        counter_message="THIS IS THE COUNTER MESSAGE THAT SHOULD BE STORED!",
        confidence=0.99,
        timestamp=datetime.now()
    )
    
    print(f"Prepared Record: {test_record.dict()}")
    
    # Save to Firebase
    doc_id = firebase_service.save_message(test_record)
    
    if doc_id:
        print(f"SUCCESS: Message saved with ID: {doc_id}")
        
        # Verify by fetching it back
        from config.firebase_config import db
        data = db.collection("messages").document(doc_id).get().to_dict()
        print(f"\nFetched Data from Firestore for {doc_id}:")
        print(f"Counter Message in DB: {data.get('counter_message')}")
        print(f"Confidence in DB:      {data.get('confidence')}")
        
        if data.get('counter_message') == "THIS IS THE COUNTER MESSAGE THAT SHOULD BE STORED!":
            print("\nVERIFICATION PASSED: The counter_message is correctly stored in Firebase.")
        else:
            print("\nVERIFICATION FAILED: counter_message mismatch.")
    else:
        print("FAILED: Could not save message to Firebase.")

if __name__ == "__main__":
    test_storage()
