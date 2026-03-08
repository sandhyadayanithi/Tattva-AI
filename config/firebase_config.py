import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initializes Firebase app using a service account JSON file from FIREBASE_KEY_PATH or default."""
    try:
        if not firebase_admin._apps:
            # Look for the credentials file from environment variables
            cred_path = os.getenv("FIREBASE_KEY_PATH", "service_account.json")
            logger.info(f"Using Firebase credentials from path: {cred_path}")
            
            if not os.path.exists(cred_path):
                logger.warning(f"Firebase credentials not found at {os.path.abspath(cred_path)}. Ensure it exists for Firestore functionality.")
                return None
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully.")
        
        return firestore.client()
    except Exception as e:
        logger.error(f"Error initializing Firebase: {str(e)}")
        return None

# Singleton-like Firestore client instance
db = initialize_firebase()
