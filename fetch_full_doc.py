from config.firebase_config import db
import json

def fetch_document():
    doc_ref = db.collection("messages").document("message_id_1772902073")
    data = doc_ref.get().to_dict()
    print("--- FULL FIRESTORE DATA ---")
    if data:
        print(json.dumps(data, indent=2, default=str))
    else:
        print("Document not found!")

if __name__ == "__main__":
    fetch_document()
