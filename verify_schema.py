from services.firebase_service import firebase_service
import json

def verify_latest_schema():
    print("Fetching recent messages...")
    messages = firebase_service.get_recent_messages()
    if not messages:
        print("No messages found in Firestore.")
        return

    # Look for a message that has the new schema (ai_response or fact_check fields)
    latest = messages[0]
    
    print("\n--- Latest Message Record ---")
    print(json.dumps(latest, indent=2))
    print("------------------------------\n")
    
    # Check for absence of root-level fields
    root_fields = ["verdict", "explanation", "counter_message", "confidence", "virality_score"]
    found_root = [f for f in root_fields if f in latest]
    
    if found_root:
        print(f"FAILED: Found redundant root-level fields: {found_root}")
    else:
        print("SUCCESS: No redundant root-level fields found.")
        
    # Check for presence of nested objects
    if "fact_check" in latest and isinstance(latest["fact_check"], dict):
        print("SUCCESS: 'fact_check' object found.")
        fc = latest["fact_check"]
        required_fc = ["verdict", "explanation", "counter_message", "confidence", "virality_score", "cached"]
        missing_fc = [f for f in required_fc if f not in fc]
        if missing_fc:
            print(f"WARNING: 'fact_check' is missing fields: {missing_fc}")
        else:
            print("SUCCESS: 'fact_check' has all required fields.")
    else:
        print("FAILED: 'fact_check' object missing or invalid.")
        
    if "ai_response" in latest and isinstance(latest["ai_response"], dict):
        print("SUCCESS: 'ai_response' object found.")
    else:
        print("FAILED: 'ai_response' object missing or invalid.")

if __name__ == "__main__":
    verify_latest_schema()
