import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    "test": "hello",
    "status": "working"
}

db.collection("debug").add(data)

print("Document added successfully")