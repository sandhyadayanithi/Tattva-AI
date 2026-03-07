# Tattva-AI Database & Vector Service Setup

This service layer provides Firebase Firestore integration for persistent message storage and ChromaDB for semantic claim caching.

## 1. Firebase Firestore Setup
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Create a new project (or use an existing one).
3. In Project Settings > Service Accounts, click **Generate new private key**.
4. Download the JSON file and save it in the root of this project as `service_account.json`. (Or update `FIREBASE_KEY_PATH` in `.env`).
5. Ensure the Firestore Database is created in the Firebase console.

## 2. ChromaDB (Vector Search)
- ChromaDB stores data locally in the `./db/chroma` directory.
- It uses the `sentence-transformers` library to generate embeddings for claims.
- The `VectorService` uses cosine similarity (threshold default: 0.85) to find similar claims.

## 3. Project Structure
- `services/firebase_service.py`: CRUD for Firestore message logs.
- `services/vector_service.py`: Semantic caching of fact-checked claims.
- `models/message_model.py`: Shared Pydantic schema for consistency.
- `config/firebase_config.py`: Firebase initialization logic.
- `utils/logger.py`: Standard logging for all modules.

## 4. Example Usage
The services are already integrated into `main.py`. You can test the endpoints for recent messages or claim storage if you run the FastAPI app locally.

```bash
# Run the FastAPI app
python -m uvicorn main:app --reload

# Test retrieval (after saving some messages)
curl http://localhost:8000/messages/recent
```
