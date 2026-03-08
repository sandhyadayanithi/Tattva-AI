from config.firebase_config import db
from google.cloud import firestore

if not db:
    print("DB is None!")
    exit(1)

print(f"Project ID: {db.project}")

collections = list(db.collections())
print(f"Total Collections found: {len(collections)}")
for col in collections:
    print(f"- {col.id}")
    docs = list(col.limit(2).stream())
    print(f"  (Found {len(docs)} docs sample)")
    for doc in docs:
        print(f"    - ID: {doc.id}")

# Specifically check 'messages'
col_msg = db.collection("messages")
docs_msg = list(col_msg.limit(2).stream())
print(f"\nSpecific check for 'messages' collection: Found {len(docs_msg)} documents.")
for d in docs_msg:
    print(f"  - {d.id}")
