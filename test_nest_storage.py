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

    message = MessageRecord(
        transcript="Test transcription",
        claim="Test claim",
        verdict="FALSE",
        explanation="This is a test explanation.",
        virality_score=4,
        virality_reason="Test reason.",
        counter_message="This is a test counter message.",
        language="English",
        category="health"
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
    
    # Validation of Standardized Schema
    required_fields = ["transcript", "claim", "verdict", "explanation", "virality_score", "virality_reason", "language", "category", "created_at"]
    errors = []
    for field in required_fields:
        if field not in saved:
            errors.append(f"Required field missing: {field}")
            
    if "fact_check" in saved:
        errors.append("Old nested 'fact_check' found")
    if "ai_response" in saved:
        errors.append("Old nested 'ai_response' found")
        
    if errors:
        print("\nVERIFICATION FAILED:")
        for err in errors:
            print(f"- {err}")
    else:
        print("\nVERIFICATION SUCCESSFUL: Nested schema correctly implemented and redundant fields removed.")

if __name__ == "__main__":
    asyncio.run(test_nested_storage())
