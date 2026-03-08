from config.firebase_config import db
if not db:
    print("DB is None!")
    exit(1)

col = db.collection("fact_checks")
docs = col.limit(1).stream()
for doc in docs:
    print(f"Document ID: {doc.id}")
    data = doc.to_dict()
    print("Fields:")
    for k, v in data.items():
        print(f"  - {k}: {type(v).__name__}")
