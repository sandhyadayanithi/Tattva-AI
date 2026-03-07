import chromadb
import os

persist_directory = "./vector_db"
client = chromadb.PersistentClient(path=persist_directory)

# Get all collections
collections = [c.name for c in client.list_collections()]
print(f"Collections found: {collections}")

# Migration Logic: If claims_cache exists but claims is empty/missing
if "claims_cache" in collections and "claims" not in collections:
    print("\nMigrating data from 'claims_cache' to 'claims'...")
    old_col = client.get_collection("claims_cache")
    new_col = client.create_collection("claims", metadata={"hnsw:space": "cosine"})
    
    data = old_col.get(include=["embeddings", "metadatas", "documents"])
    if data["ids"]:
        new_col.add(
            ids=data["ids"],
            embeddings=data["embeddings"],
            metadatas=data["metadatas"],
            documents=data["documents"]
        )
        print(f"Successfully migrated {len(data['ids'])} records.")
    
    # Optionally delete the old one to keep it clean
    # client.delete_collection("claims_cache")

# Final Check
if "claims" in [c.name for c in client.list_collections()]:
    collection = client.get_collection("claims")
    results = collection.get()
    print(f"\nTotal claims in 'claims' collection: {len(results.get('ids', []))}")
    if len(results.get('ids', [])) > 0:
        print("\nStored Claims Sample:")
        for doc in results['documents'][-3:]:
            print(f"- {doc}")
else:
    print("\nNo 'claims' collection found yet.")

