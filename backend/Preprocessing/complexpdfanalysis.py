# This script uses Google Cloud Vision API to extract text from PDF files by first converting each page to an image.
# It is useful for extracting text from scanned PDFs or PDFs with complex layouts.

import sys, pathlib, os
from pdf2image import convert_from_path
from google.cloud import vision
from google.api_core.client_options import ClientOptions
from dotenv import load_dotenv

load_dotenv()
filename1 = "Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-08-02_BFS-.pdf"
filename2 = "Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-08-04_Module-2-.pdf"
filename3 = "Data/pdf/FALLSEM2025-26_BCSE307L_TH_VL2025260101612_2025-07-11_Reference-Material-I.pdf"

fname = filename3

def extract_text_from_pdf_with_vision(pdf_path):
    """
    Converts each page of the PDF to an image, then uses Google Cloud Vision API to extract text from each image.
    Returns the combined text from all pages.
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY not found. Make sure you have a .env file with the key.")
    client_options = ClientOptions(api_key=api_key)
    client = vision.ImageAnnotatorClient(client_options=client_options)
    all_text = []
    for i, image in enumerate(images):
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        content = img_byte_arr.getvalue()
        image_vision = vision.Image(content=content)
        response = client.document_text_detection(image=image_vision)
        if response.error.message:
            raise Exception(
                f"Error from Vision API: {response.error.message}\nSee https://cloud.google.com/apis/design/errors for more info."
            )
        text = response.full_text_annotation.text if response.full_text_annotation.text else ""
        all_text.append(text)
    return chr(12).join(all_text)

# Run the extraction and save the result to a file
text = extract_text_from_pdf_with_vision(fname)
pathlib.Path(fname + "Cloudvision" + ".txt").write_text(text, encoding="utf-8")


#filename1 = FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-08-02_BFS-.pdf
#filename2 = FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-08-04_Module-2-.pdf
#filename3 = FALLSEM2025-26_BCSE307L_TH_VL2025260101612_2025-07-11_Reference-Material-I.pdf