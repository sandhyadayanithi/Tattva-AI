import os
import sys
from datetime import datetime
from google.cloud import firestore
from dotenv import load_dotenv

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.firebase_config import db
from services.firebase_service import firebase_service
from models.message_model import MessageRecord
from utils.text_utils import normalize_transcript

load_dotenv()

def classify_claim(claim):
    """Simple keyword-based classification for migration."""
    claim_lower = claim.lower()
    if any(k in claim_lower for k in ["health", "vaccine", "doctor", "medicine", "cure", "virus", "cancer", "hospital"]):
        return "health"
    if any(k in claim_lower for k in ["election", "vote", "government", "politician", "party", "ballot", "minister"]):
        return "election"
    if any(k in claim_lower for k in ["religion", "god", "temple", "church", "faith", "prayer"]):
        return "religion"
    if any(k in claim_lower for k in ["finance", "money", "bank", "stock", "investment", "tax", "crypto"]):
        return "finance"
    return "health"  # Default

def migrate():
    print("Starting Firestore Migration...")
    
    old_collection = db.collection("messages")
    new_collection = db.collection("fact_checks")
    
    docs = old_collection.stream()
    count = 0
    success = 0
    fail = 0
    
    for doc in docs:
        count += 1
        data = doc.to_dict()
        print(f"Processing document: {doc.id}")
        
        try:
            # 1. Map fields
            transcript = data.get("transcription") or data.get("transcript") or "No transcript available"
            claim = data.get("claim") or "No claim extracted"
            
            # Infer verdict (handle case-sensitivity)
            verdict_raw = data.get("verdict") or "FALSE"
            if isinstance(verdict_raw, str):
                verdict = "TRUE" if verdict_raw.upper() in ["TRUE", "YES", "VERIFIED"] else "FALSE"
            else:
                verdict = "FALSE"
            
            explanation = data.get("explanation") or "Historical record."
            virality_score = data.get("virality_score") or 5
            virality_reason = data.get("virality_reason") or "Legacy record from previous system."
            counter_message = data.get("counter_message")
            language = data.get("language") or "English"
            category = data.get("category") or classify_claim(claim)
            created_at = data.get("timestamp") or data.get("created_at") or firestore.SERVER_TIMESTAMP
            
            # 2. Create Standardized Record (always normalize transcript for cache consistency)
            standardized_data = {
                "transcript": normalize_transcript(transcript),
                "claim": claim,
                "verdict": verdict,
                "explanation": explanation,
                "virality_score": int(virality_score),
                "virality_reason": virality_reason,
                "counter_message": counter_message,
                "language": language,
                "category": category,
                "created_at": created_at
            }
            
            # 3. Validate (using firebase_service logic)
            is_valid, errors = firebase_service.validate_document(standardized_data)
            if not is_valid:
                print(f"  Validation failed for {doc.id}: {', '.join(errors)}")
                fail += 1
                continue
            
            # 4. Write to new collection
            new_collection.document(doc.id).set(standardized_data)
            success += 1
            print(f"  Migrated {doc.id} successfully.")
            
        except Exception as e:
            print(f"  Error migrating {doc.id}: {e}")
            fail += 1
            
    print("\nMigration Complete!")
    print(f"Total processed: {count}")
    print(f"Successfully migrated: {success}")
    print(f"Failed: {fail}")

if __name__ == "__main__":
    migrate()
unlink_audio_files = True # Hypothetical flag if we wanted to cleanup
