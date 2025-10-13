import re
import os

#create chunks such that each page is in its own chunk
# the text file of a doc and ppt has pages numbers. Search for "slide" or "page" to find page breaks
#page1 complete
#slide1 complete

# chunk_package = {
#     "id": "textbook_chapter_3_chunk_001",  # A unique ID for this chunk
#     "source_document": "textbook_chapter_3.pdf",
#     "page_number": 42,
#     "keywords": ['Best first search', 'heuristic search', 'Priority queue'],
#     "text": "The Best first search uses the concept of a Priority queue and heuristic search...",
#     "embedding": [0.012, -0.045, 0.088, ..., -0.021] # The 384-element vector
# }

def create_chunks(file_path: str):
    """
    Chunks a text file from a .pdf.txt or .pptx.txt into page/slide based chunks.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of chunk packages, where each package is a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    base_filename = os.path.basename(file_path)
    if base_filename.endswith('.pdf.txt'):
        source_document = base_filename[:-4]
        delimiter_pattern = r'page\d+ complete'
    elif base_filename.endswith('.pptx.txt'):
        source_document = base_filename[:-4]
        delimiter_pattern = r'slide\d+ complete'
    else:
        raise ValueError("Unsupported file type. Only .pdf.txt and .pptx.txt are supported.")

    # Split the text by the delimiter
    # The delimiter is kept in the resulting list, so we process pairs of (text, delimiter)
    parts = re.split(f'({delimiter_pattern})', text)
    
    chunks = []
    chunk_text = parts[0].strip()
    page_number = 1

    if chunk_text:
        chunk_id = f"{os.path.splitext(source_document)[0]}_chunk_{page_number:03d}"
        chunks.append({
            "id": chunk_id,
            "source_document": source_document,
            "page_number": page_number,
            "keywords": [],  # To be filled later
            "text": chunk_text,
            "embedding": None # To be filled later
        })

    # Process the rest of the parts
    for i in range(1, len(parts), 2):
        delimiter = parts[i]
        chunk_text = parts[i+1].strip() if (i+1) < len(parts) else ""
        
        page_number_match = re.search(r'\d+', delimiter)
        if page_number_match:
            page_number = int(page_number_match.group(0))

        if chunk_text:
            chunk_id = f"{os.path.splitext(source_document)[0]}_chunk_{page_number + 1:03d}"
            chunks.append({
                "id": chunk_id,
                "source_document": source_document,
                "page_number": page_number + 1,
                "keywords": [],
                "text": chunk_text,
                "embedding": None
            })

    return chunks