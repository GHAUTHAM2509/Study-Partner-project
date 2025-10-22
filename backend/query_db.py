import chromadb
from sentence_transformers import SentenceTransformer
import os
import sys
import argparse

def query_database(collection_name: str, query_text: str, n_results: int = 5):
    """
    Connects to the ChromaDB, queries a collection, and prints the results.
    """
    # --- 1. SETUP ---
    print("Loading embedding model...")
    try:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Error loading sentence transformer model: {e}")
        print("Please ensure you have an internet connection and sentence-transformers is installed.")
        return

    print("Connecting to vector database...")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Database', 'db'))
    
    if not os.path.exists(db_path):
        print(f"Error: Database path not found at {db_path}")
        print("Please ensure you have run the ingestion script to create the database.")
        return

    try:
        client = chromadb.PersistentClient(path=db_path)
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        return

    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
        print(f"Error: Could not get collection '{collection_name}'. {e}")
        collections = client.list_collections()
        if collections:
            print(f"Available collections: {[c.name for c in collections]}")
        else:
            print("No collections found in the database.")
        return

    # --- 2. QUERY ---
    print(f"\\nQuerying collection '{collection_name}' with: '{query_text}'")

    query_embedding = embedding_model.encode(query_text).tolist()

    retrieved_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # --- 3. DISPLAY RESULTS ---
    documents = retrieved_results.get('documents', [[]])[0]
    metadatas = retrieved_results.get('metadatas', [[]])[0]
    distances = retrieved_results.get('distances', [[]])[0]

    if not documents:
        print("No results found.")
        return

    print("\\n--- QUERY RESULTS ---\\n")
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        print(f"--- Result {i+1} (Distance: {dist:.4f}) ---")
        print(f"Source: {meta.get('source', 'N/A')}, Page: {meta.get('page', 'N/A')}")
        print(f"Keywords: {meta.get('keywords', 'N/A')}")
        print(f"Text: {doc[:500]}...") # Print first 500 chars
        print("-" * 20)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query a ChromaDB collection from the terminal.")
    parser.add_argument("collection", type=str, help="The name of the collection to query.")
    parser.add_argument("query", type=str, help="The text query to search for.")
    parser.add_argument("-n", "--n_results", type=int, default=3, help="The number of results to return.")
    
    args = parser.parse_args()
    
    query_database(args.collection, args.query, args.n_results)
