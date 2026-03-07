from ai.fact_checker import FactCheckerEngine
from models.message_model import MessageRecord
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_virality_and_storage_data():
    print("--- Testing Virality Score & Data Schema ---")
    engine = FactCheckerEngine(use_llm=True)
    
    # Using a sensational claim to trigger high virality risk
    claim = "SHOCKING: Drinking 5 liters of boiling water instantly kills the COVID-19 virus!! SHARE THIS NOW!!"
    print(f"Testing claim: {claim}")
    
    evidence = [
        "COVID-19 is a respiratory virus. Boiling water is harmful and can cause severe burns, and does not cure the virus.",
        "The WHO warns against drinking extremely hot liquids as a cure for COVID-19."
    ]
    
    result = engine.generate_verdict(claim, evidence)
    print("\n--- LLM Response ---")
    print(json.dumps(result, indent=2))
    
    # Verify fields from new prompt
    required_fields = ["verdict", "category", "virality_score", "virality_reason_en", "explanation_en", "counter_message_en"]
    missing = [f for f in required_fields if f not in result]
    
    if not missing:
        print("\n✅ All required JSON fields present.")
    else:
        print(f"\n❌ Missing fields: {missing}")

    if result.get("virality_score", 0) > 7:
        print("✅ Virality score correctly identified as High for sensational claim.")
    else:
        print(f"⚠️ Virality score: {result.get('virality_score')}. Might need more drastic prompt tuning.")

    # Test MessageRecord mapping
    print("\n--- Testing MessageRecord Mapping ---")
    record = MessageRecord(
        transcript=claim,
        claim=claim,
        verdict=result["verdict"],
        explanation=result["explanation_en"],
        virality_score=result["virality_score"],
        virality_reason=result["virality_reason_en"],
        counter_message=result["counter_message_en"],
        language="English",
        category=result["category"]
    )
    
    print("✅ MessageRecord created successfully.")
    print(f"Firestore Payload Preview: {record.dict()}")

if __name__ == "__main__":
    test_virality_and_storage_data()
