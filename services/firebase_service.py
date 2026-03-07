from datetime import datetime
from google.cloud import firestore
from config.firebase_config import db
from models.message_model import MessageRecord
from utils.logger import logger


class FirebaseService:
    def __init__(self, collection_name="messages"):
        self.collection = db.collection(collection_name) if db else None

    def save_message(self, message: MessageRecord):
        """Stores processed message records in a 'messages' collection."""
        if not self.collection:
            logger.error("Firebase not initialized. Cannot save message.")
            return None
        
        try:
            # Convert MessageRecord to dictionary
            message_data = message.dict()
            
            # Generate a cleaner document ID using timestamp if not provided
            doc_id = message_data.get("id")
            if not doc_id:
                ts = int(message_data.get("timestamp", datetime.now()).timestamp())
                doc_id = f"message_id_{ts}"
            
            doc_ref = self.collection.document(doc_id)
            
            # Fill document ID back into dict if it's new
            message_data["id"] = doc_ref.id
            
            # Save to Firestore
            doc_ref.set(message_data)
            logger.info(f"Message saved successfully to Firestore with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error saving message to Firestore: {str(e)}")
            return None

    def get_recent_messages(self, limit=20):
        """Retrieves recent processed message records from the messages collection."""
        if not self.collection:
            logger.error("Firebase not initialized.")
            return []
        
        try:
            # Firestore query for recent messages ordered by timestamp descending
            docs = self.collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
            messages = [doc.to_dict() for doc in docs]
            return messages
        except Exception as e:
            logger.error(f"Error retrieving recent messages from Firestore: {str(e)}")
            return []

    def get_messages_by_user(self, user_number):
        """Retrieves processed message records for a specific user number."""
        if not self.collection:
            logger.error("Firebase not initialized.")
            return []
        
        try:
            # Firestore query filtering by user_number
            docs = self.collection.where("user_number", "==", user_number).stream()
            messages = [doc.to_dict() for doc in docs]
            return messages
        except Exception as e:
            logger.error(f"Error retrieving messages for user {user_number} from Firestore: {str(e)}")
            return []

# Example helper function if needed for simple functional calls
firebase_service = FirebaseService()
