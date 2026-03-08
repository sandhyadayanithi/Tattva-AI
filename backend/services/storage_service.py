import os
import firebase_admin
from firebase_admin import storage, credentials
from utils.logger import logger
from datetime import datetime, timedelta

class StorageService:
    def __init__(self):
        self.bucket = None
        try:
            # Check if app is already initialized
            if not firebase_admin._apps:
                cred_path = "service_account.json"
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred, {
                        'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")
                    })
                else:
                    logger.warning("service_account.json not found. Storage service might fail.")
            
            bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
            if bucket_name:
                self.bucket = storage.bucket()
                logger.info(f"Firebase Storage bucket '{bucket_name}' initialized.")
            else:
                logger.warning("FIREBASE_STORAGE_BUCKET env var not set.")
                
        except Exception as e:
            logger.error(f"Error initializing Storage Service: {e}")

    def upload_file(self, local_path, folder="media"):
        """Uploads a file to Firebase Storage and returns the public URL."""
        if not self.bucket:
            logger.error("Storage bucket not initialized.")
            return local_path # Fallback to local path

        try:
            file_name = os.path.basename(local_path)
            blob_path = f"{folder}/{file_name}"
            blob = self.bucket.blob(blob_path)
            
            # Explicitly set content type based on extension
            ext = os.path.splitext(local_path)[1].lower()
            content_type = "application/octet-stream"
            if ext in [".jpg", ".jpeg"]: content_type = "image/jpeg"
            elif ext == ".png": content_type = "image/png"
            elif ext == ".ogg": content_type = "audio/ogg"
            elif ext == ".mp4": content_type = "video/mp4"
            
            blob.upload_from_filename(local_path, content_type=content_type)
            
            # Make the file public (optional, or use signed URLs)
            # For simplicity, we'll generate a long-lived signed URL or make it public if allowed
            blob.make_public()
            return blob.public_url
            
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            return local_path

storage_service = StorageService()
