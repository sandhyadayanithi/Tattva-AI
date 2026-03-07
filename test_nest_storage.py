import os
import asyncio
from models.message_model import MessageRecord
from services.firebase_service import firebase_service
from datetime import datetime

async def test_nested_storage():
    print("Simulating fact-check result...")
    fact_result = {
        "verdict_en": "False",
        "explanation_en": "This is a test explanation.",
        "counter_message_en": "This is a test counter message.",
        "confidence_score": 0.85,
        "virality_score": 4,
        "cached": False,
        "some_raw_data": "extra info"
    }

    print("Creating MessageRecord with nested schema...")
    fact_check_data = {
        "verdict": fact_result.get("verdict_en"),
        "explanation": fact_result.get("explanation_en"),
        "counter_message": fact_result.get("counter_message_en"),
        "confidence": fact_result.get("confidence_score"),
        "virality_score": fact_result.get("virality_score"),
        "cached": fact_result.get("cached")
    }

    message = MessageRecord(
        user_number="test_user_123",
        claim="Test claim",
        transcription="Test transcription",
        fact_check=fact_check_data,
        ai_response=fact_result,
        timestamp=datetime.now()
    )

    print("Saving to Firestore...")
    doc_id = firebase_service.save_message(message)
    if not doc_id:
        print("Failed to save message.")
        return

    print(f"Saved message with ID: {doc_id}")
    
    print("Retrieving saved document...")
    # Refreshing from Firestore
    messages = firebase_service.get_recent_messages(limit=1)
    if not messages:
        print("Could not retrieve messages.")
        return
        
    saved = messages[0]
    
    print("\n--- Verified Firestore Structure ---")
    import json
    print(json.dumps(saved, indent=2))
    
    # Validation
    root_redundant = ["verdict", "explanation", "counter_message", "confidence", "virality_score"]
    errors = []
    for field in root_redundant:
        if field in saved:
            errors.append(f"Redundant root field found: {field}")
            
    if "fact_check" not in saved:
        errors.append("fact_check object missing")
    if "ai_response" not in saved:
        errors.append("ai_response object missing")
        
    if errors:
        print("\nVERIFICATION FAILED:")
        for err in errors:
            print(f"- {err}")
    else:
        print("\nVERIFICATION SUCCESSFUL: Nested schema correctly implemented and redundant fields removed.")

if __name__ == "__main__":
    asyncio.run(test_nested_storage())
