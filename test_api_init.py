from dotenv import load_dotenv
load_dotenv()
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_init")

print(f"DEBUG: FIREBASE_KEY_PATH = {os.getenv('FIREBASE_KEY_PATH')}")
print(f"DEBUG: File exists? {os.path.exists(os.getenv('FIREBASE_KEY_PATH', ''))}")

from config.firebase_config import db
print(f"DEBUG: db object = {db}")

from services.firebase_service import firebase_service
print(f"DEBUG: firebase_service.collection = {firebase_service.collection}")

if firebase_service.collection:
    print("DEBUG: Executing query...")
    messages = firebase_service.get_recent_messages(limit=5)
    print(f"DEBUG: Received {len(messages)} messages.")
    for m in messages:
        print(f"  - {m.get('id')} / {m.get('claim')}")
else:
    print("DEBUG: Collection is None!")
