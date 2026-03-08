from datetime import datetime
from google.cloud import firestore
from config.firebase_config import db
from models.message_model import MessageRecord
from utils.logger import logger


class FirebaseService:
    def __init__(self, collection_name="fact_checks"):
        self.collection = db.collection(collection_name) if db else None

    def validate_document(self, data: dict):
        """Validates the document against the standardized schema rules."""
        errors = []
        if not data.get("transcript"):
            errors.append("Missing transcript")
        if not data.get("claim"):
            errors.append("Missing claim")
        
        verdict = data.get("verdict")
        if verdict not in ["TRUE", "FALSE"]:
            errors.append(f"Invalid verdict: {verdict}. Must be TRUE or FALSE.")
        
        virality_score = data.get("virality_score")
        if not isinstance(virality_score, int) or not (1 <= virality_score <= 10):
            errors.append(f"Invalid virality_score: {virality_score}. Must be between 1 and 10.")
        
        if errors:
            return False, errors
        return True, []

    def check_transcript_cache(self, normalized_transcript: str):
        """
        Queries Firestore for a previously stored result with the same normalized transcript.
        Returns the stored document dict if found, otherwise None.
        """
        if not self.collection:
            logger.error("Firebase not initialized. Cannot check transcript cache.")
            return None
        try:
            docs = (
                self.collection
                .where("transcript", "==", normalized_transcript)
                .limit(1)
                .stream()
            )
            results = list(docs)
            if results:
                logger.info("Transcript cache hit – returning stored result.")
                return results[0].to_dict()
            logger.info("No transcript match – running full pipeline.")
            return None
        except Exception as e:
            logger.error(f"Error checking transcript cache: {e}")
            return None

    def save_message(self, message: MessageRecord):
        """Stores standardized fact-check records in the 'fact_checks' collection."""
        if not self.collection:
            logger.error("Firebase not initialized. Cannot save message.")
            return None
        
        try:
            # Convert MessageRecord to dictionary
            message_data = message.dict()
            
            # Use current Firestore timestamp for created_at
            message_data["created_at"] = firestore.SERVER_TIMESTAMP
            
            # Validate before writing
            is_valid, errors = self.validate_document(message_data)
            if not is_valid:
                logger.error(f"Validation failed for Firestore document: {', '.join(errors)}")
                return None

            doc_ref = self.collection.document()
            doc_ref.set(message_data)
            logger.info(f"Fact-check saved successfully to Firestore with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error saving fact-check to Firestore: {str(e)}")
            return None

    def get_recent_messages(self, limit=20):
        """Retrieves recent standardized fact-check records."""
        if not self.collection:
            logger.error("Firebase not initialized.")
            return []
        
        try:
            docs = self.collection.order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
            messages = [doc.to_dict() for doc in docs]
            return messages
        except Exception as e:
            logger.error(f"Error retrieving recent fact-checks from Firestore: {str(e)}")
            return []

# Example helper function if needed for simple functional calls
firebase_service = FirebaseService()
