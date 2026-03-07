import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from utils.logger import logger
from datetime import datetime

class VectorService:
    def __init__(self, collection_name="claims_cache", persist_directory="./vector_db"):
        """Initializes ChromaDB client and sets up the claims collection."""
        # Use a lightweight, efficient embedding model
        # Using SentenceTransformer as an external embedding function for the collection
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        
        # Ensure persist directory exists
        if not os.path.exists("./vector_db"):
            os.makedirs("./vector_db")
        
        # Persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create the collection for claims
        # We specify cosine similarity as requested by the task
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"ChromaDB collection '{collection_name}' initialized in {persist_directory}.")

    def store_claim(self, claim_text: str, fact_check_result: dict):
        """Generates embedding for a claim and stores it with its full JSON result."""
        try:
            # Generate claim vector embedding
            embedding = self.model.encode(claim_text).tolist()
            
            # Use deterministic ID based on claim text (to avoid duplicates)
            import hashlib
            claim_id = hashlib.md5(claim_text.encode()).hexdigest()
            
            import json
            
            # Store in ChromaDB collection
            self.collection.add(
                ids=[claim_id],
                embeddings=[embedding],
                metadatas=[{
                    "verdict": str(fact_check_result.get("verdict", "")),
                    "explanation": str(fact_check_result.get("explanation", "")),
                    "full_response": json.dumps(fact_check_result),
                    "timestamp": datetime.now().isoformat()
                }],
                documents=[claim_text]
            )
            logger.info(f"Claim stored in semantic cache: {claim_text[:50]}...")
            return claim_id
        except Exception as e:
            logger.error(f"Error storing claim in vector DB: {str(e)}")
            return None

    def find_similar_claim(self, claim_text: str, threshold: float = 0.85):
        """Searches for semantically similar claims in the cache."""
        try:
            # Generate query vector embedding
            query_embedding = self.model.encode(claim_text).tolist()
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=1,
                include=["metadatas", "distances", "documents"]
            )
            
            if results["ids"] and len(results["ids"][0]) > 0:
                # distance is 1 - cosine_similarity for 'cosine' space (lower is better, similarity is higher)
                score = 1 - results["distances"][0][0]
                
                if score >= threshold:
                    logger.info(f"Semantic match found with confidence score {score:.2f}")
                    import json
                    full_response_str = results["metadatas"][0][0].get("full_response")
                    
                    if full_response_str:
                        cached_result = json.loads(full_response_str)
                    else:
                        cached_result = {
                            "verdict": results["metadatas"][0][0].get("verdict", ""),
                            "explanation": results["metadatas"][0][0].get("explanation", "")
                        }
                    
                    cached_result["claim"] = results["documents"][0][0]
                    cached_result["score"] = score
                    return cached_result
                else:
                    logger.info(f"No semantic match found (highest score {score:.2f} < {threshold})")
            
            return None
        except Exception as e:
            logger.error(f"Error searching vector DB: {str(e)}")
            return None

# Singleton instance to be used across the app
vector_service = VectorService()

def initialize_vector_db():
    """Explicit initializer if needed elsewhere."""
    return vector_service
