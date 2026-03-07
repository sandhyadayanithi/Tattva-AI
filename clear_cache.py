from services.vector_service import vector_service

def clear_cache():
    print("Clearing ChromaDB collection 'claims'...")
    try:
        # Re-initialize collection by deleting and letting the service recreate it
        vector_service.client.delete_collection("claims")
        print("Collection 'claims' deleted successfully.")
    except Exception as e:
        print(f"Error (probably already deleted): {e}")

if __name__ == "__main__":
    clear_cache()
