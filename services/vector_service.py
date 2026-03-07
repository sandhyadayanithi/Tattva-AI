import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from utils.logger import logger


class VectorService:
    def __init__(self, collection_name="claims_cache", persist_directory="./db/chroma"):
        """Initializes ChromaDB client and sets up the claims collection."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight, efficient model
        
        # Ensure persist directory exists
        if not os.path.exists("./db"):
            os.makedirs("./db")
        
        # In-memory or Persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create the collection for claims
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            metadata={"hnsw:space": "cosine"} # Use cosine similarity
        )
        logger.info(f"ChromaDB collection '{collection_name}' initialized.")

    def store_claim_embedding(self, claim: str, verdict: str, explanation: str):
        """Generates embedding for a claim and stores it with its verdict/explanation."""
        try:
            # Generate claim vector embedding
            embedding = self.model.encode(claim).tolist()
            
            # Use hash of claim (or simple unique string) for ID
            claim_id = str(hash(claim))
            
            # Store in ChromaDB collection
            self.collection.add(
                ids=[claim_id],
                embeddings=[embedding],
                metadatas=[{
                    "verdict": verdict,
                    "explanation": explanation
                }],
                documents=[claim]
            )
            logger.info(f"Claim stored in vector cache: {claim}")
            return claim_id
        except Exception as e:
            logger.error(f"Error storing claim embedding: {str(e)}")
            return None

    def search_similar_claim(self, claim: str, threshold: float = 0.85):
        """Searches for semantically similar claims in the cache."""
        try:
            # Generate claim vector embedding
            query_embedding = self.model.encode(claim).tolist()
            
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
                    logger.info(f"Similar claim found in cache with confidence score {score:.2f}")
                    return {
                        "claim": results["documents"][0][0],
                        "verdict": results["metadatas"][0][0]["verdict"],
                        "explanation": results["metadatas"][0][0]["explanation"],
                        "confidence": score
                    }
                else:
                    logger.info(f"No sufficiently similar claim found (highest score {score:.2f} < {threshold})")
            
            return None
        except Exception as e:
            logger.error(f"Error searching similar claim: {str(e)}")
            return None

# Singleton-style VectorService instance
vector_service = VectorService()
