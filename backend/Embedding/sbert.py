sample_chunk = {'id': 'FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI_chunk_010', 'source_document': 'FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI.pptx', 'page_number': 10, 'keywords': ['Social Media Social', 'Media Social Media', 'digital world', 'Data Security', 'growing very rapidly', 'AI', 'various travel related works', 'Travel industries', 'travel industries', 'data'], 'text': 'Cont…\nAI in Data Security\nThe security of data is crucial for every company and cyber-attacks are growing very rapidly in the digital world. AI can be used to make your data more safe and secure. Some examples such as AEG bot, AI2 Platform,are used to determine software bug and cyber-attacks in a better way.\n AI in Social Media\nSocial Media sites such as Facebook, Twitter, and Snapchat contain billions of user profiles, which need to be stored and managed in a very efficient way. AI can organize and manage massive amounts of data. AI can analyze lots of data to identify the latest trends, hashtag, and requirement of different users.\nAI in Travel & Transport\nAI is becoming highly demanding for travel industries. AI is capable of doing various travel related works such as from making travel arrangement to suggesting the hotels, flights, and best routes to the customers. Travel industries are using AI-powered chatbots which can make human-like interaction with customers for better and fast response.', 'embedding': None}

from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(chunk):
    """
    Generates an embedding for the text in a chunk using 'all-MiniLM-L6-v2'.
    """
    text_to_embed = chunk['text']
    embedding = model.encode(text_to_embed)
    chunk['embedding'] = embedding.tolist()  # Convert numpy array to list for easier handling (e.g., JSON)
    return chunk
def create_embedding_for_chunks(chunks):
    return [create_embedding(chunk) for chunk in chunks]

if __name__ == "__main__":
    print("Original chunk:")
    print(sample_chunk)
    print("\n")
    
    updated_chunk = create_embedding(sample_chunk)
    print(updated_chunk)
    print("Chunk with embedding:")
    # To avoid printing the full large embedding, we'll show a confirmation.
    if updated_chunk['embedding']:
        print(f"Embedding created with length: {len(updated_chunk['embedding'])}")
        # print("First 5 values:", updated_chunk['embedding'][:5])
    else:
        print("Embedding creation failed.")

