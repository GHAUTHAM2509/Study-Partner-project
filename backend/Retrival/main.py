import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
from dotenv import load_dotenv
import redis
from  utils.api_key_manager import get_next_api_key
import re

# --- 1. SETUP ---
# This section initializes the necessary components.

# Load environment variables from the .env file in the project root
load_dotenv()

# It's recommended to set your Gemini API key as an environment variable for security.
# In your terminal, run: export GEMINI_API_KEY='YOUR_API_KEY'
try:
    key = get_next_api_key()
    genai.configure(api_key=os.environ[key])
    print(os.environ[key])
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit()


# Initialize the embedding model, which must be the same one used to create the embeddings in your database.
print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2') 

# Initialize the ChromaDB client and get the collection where your notes are stored.
print("Connecting to vector database...")
# Connect to the persistent database stored in the 'Database/db' directory
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'db'))
client = chromadb.PersistentClient(path=db_path)

# --- 2. THE RAG LOOP ---
# This function encapsulates the entire Retrieval-Augmented Generation process.

def answer_question(user_question, course_name):
    """
    Takes a user's question, retrieves relevant context from the database,
    and generates a synthesized answer using an LLM.
    """
    print(f"\nProcessing question: '{user_question}' for course: '{course_name}'")

    # Map course_name to collection_name
    course_to_collection_map = {
        "database-systems": "database",
        "operating-systems": "operating_systems",
        "cloud-computing": "aws"
    }
    collection_name = course_to_collection_map.get(course_name)

    if not collection_name:
        return f"Error: No collection found for course '{course_name}'."

    collection = client.get_collection(name=collection_name)

    # Step 1: Embed the user's question[cite: 51].
    # The question is converted into a vector using the same model as the documents.
    query_embedding = embedding_model.encode(user_question).tolist()

    # Step 2: Query the vector database to retrieve relevant context[cite: 51].
    # The database performs a similarity search to find the most contextually relevant text chunks[cite: 47].
    print("Retrieving relevant context from notes...")
    retrieved_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=15 # Retrieve the top 5 most relevant chunks[cite: 232].
    )

    # Extract the retrieved text chunks (documents) and their metadata.
    retrieved_documents = retrieved_results['documents'][0]
    retrieved_metadatas = retrieved_results['metadatas'][0]

    # Format the retrieved context into a single string.
    context_string = "\n\n---\n\n".join(retrieved_documents)

    # Step 3: Construct a comprehensive prompt for the LLM[cite: 241].
    # This prompt includes instructions, the retrieved context, and the user's question.
    # This structure forces the LLM to use only the provided context, preventing hallucinations.
    prompt_template = """
    You are a meticulous and insightful AI research assistant. Your primary function is to help me understand and analyze my personal notes.

    Your answers MUST be based on the provided CONTEXT. Use any external knowledge do not make assumptions beyond what is written in the notes.
    Keep your answers long enough to be comprehensive but concise enough to be clear and to the point.

    Follow these rules strictly:
    1.  **Synthesize, Don't Just Find:** Do not just copy-paste snippets. Synthesize the relevant information from the context into a coherent and comprehensive answer.
    2.  **Be Honest About Gaps:** If the context does not contain the answer, state clearly: "Based on your notes, the information to answer this question isn't available." If the context is related but doesn't provide a direct answer, explain what information is available and how it relates to the question. Do not apologize.
    3.  **Format for Clarity:** Use markdown formatting like bolding for key terms and bullet points for lists to make your answers easy to read.
    4.  **Stay Concise:** Provide a direct and complete answer without unnecessary conversational filler.

    CONTEXT:
    ---
    {context}
    ---

    USER QUESTION: {question}

    ASSISTANT'S ANSWER:
    """

    final_prompt = prompt_template.format(context=context_string, question=user_question)

    # Step 4: Send the prompt to the LLM to generate the final answer.
    # The LLM synthesizes a coherent answer based *only* on the augmented context.
    print("Generating final answer with Gemini...")
    try:
        # Using 'gemini-2.0-flash' which is a more stable and specific model identifier.
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(final_prompt)
        generated_answer = response.text
    except Exception as e:
        return f"An error occurred with the Gemini API: {e}"

    # Clean the generated answer to remove any stray citation markers.
    cleaned_answer = re.sub(r'\[cite: \d+\]', '', generated_answer).strip()


    # Step 5: Append citations from the retrieved metadata.
    # This makes the answer verifiable and transforms the tool into a genuine research assistant.
    citations = set()
    for metadata in retrieved_metadatas:
        source = metadata.get('source', 'Unknown Source')
        page = metadata.get('page', 'N/A')
        citations.add(f"(Source: {source}, Page: {page})")
    
    final_answer_with_citations = f"{cleaned_answer}\n\nSources:\n" + "\n".join(sorted(list(citations)))

    return final_answer_with_citations


# --- 3. EXECUTION ---
# This is where you run the RAG loop with a specific question.

if __name__ == "__main__":
    # This is an example question. Change it to query your own document.
    # The RAG loop is triggered by a user's natural language query[cite: 50].
    my_question = "Explain Simple Reflex Agent"

    final_answer = answer_question(my_question)
    
    print("\n--- FINAL ANSWER ---")
    print(final_answer)