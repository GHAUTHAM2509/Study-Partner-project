from .chunking import create_chunks
from .sbert import create_embedding, create_embedding_for_chunks
from .keywordextraction import extract_keywords, extract_keywords_from_chunks


# chunks = create_chunks("Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-28_Module-2.pdf.txt")
# print(chunks)

# chunks = create_chunks("Data/ppts/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI.pptx.txt")
# print(chunks[0])

def process_pipeline(file_path: str):
    chunks = create_chunks(file_path)
    chunks_embedded = create_embedding_for_chunks(chunks)
    chunks_final = extract_keywords_from_chunks(chunks_embedded)
    return chunks_final

if __name__ == "__main__":
    file_path = "Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-28_Module-1.pdf.txt"
    processed_chunks = process_pipeline(file_path)
    #save it to a text file
    # with open("Data/ppts/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI_processed.txt", "w") as f:
    #     for chunk in processed_chunks:
    #         f.write(str(chunk) + "\n")
