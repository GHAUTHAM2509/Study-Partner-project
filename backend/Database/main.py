import sys
import os
import chromadb

# Add project root to Python path to resolve module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Embedding.process_pipline import process_pipeline

file_path = "Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-28_Module-1.pdf.txt"
chunk_package = process_pipeline(file_path)

list_of_packages = chunk_package

# --- 1. Create a ChromaDB Client ---
# The line below creates an in-memory instance of ChromaDB, which does not save files.
# client = chromadb.Client()

# To save the database to disk, use PersistentClient.
# This will create a 'db' directory inside your 'Database' folder to store the database files.
db_path = os.path.join(os.path.dirname(__file__), "db")
client = chromadb.PersistentClient(path=db_path)


# --- 2. Create or Get a Collection ---
# A collection is where your data will be stored. Think of it like a table in a SQL database.
collection = client.get_or_create_collection(name="ai_study_notes")


# --- 3. Prepare the data lists from your package(s) ---
ids = [pkg['id'] for pkg in list_of_packages]
embeddings = [pkg['embedding'] for pkg in list_of_packages]
documents = [pkg['text'] for pkg in list_of_packages]
metadatas = []
for pkg in list_of_packages:
    metadatas.append({
        "source": pkg['source_document'],
        "page": pkg['page_number'],
        # IMPORTANT: Convert list of keywords to a single string
        "keywords": ", ".join(pkg['keywords']) 
    })


# --- 4. Add the data to the collection ---
# You provide the lists for each corresponding field.
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas
)

print(f"Successfully added {collection.count()} item to the collection.")