# This script uses Google Cloud Vision API to generate a description for each image in a directory.
# It is useful for labeling images extracted from PDFs.

import os
from dotenv import load_dotenv
from google.cloud import vision
from google.api_core.client_options import ClientOptions

load_dotenv()

def generate_image_description(image_path):
    """
    Generates a description for the image at the given path using Google Cloud Vision API label detection.
    Returns a string describing the likely contents of the image.
    """
    api_key = os.getenv("cloud_vision_api_key")
    if not api_key:
        raise Exception("cloud_vision_api_key not found. Make sure you have a .env file with the key.")

    client_options = ClientOptions(api_key=api_key)
    client = vision.ImageAnnotatorClient(client_options=client_options)

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    if labels:
        description = "This image likely contains: " + ", ".join([label.description for label in labels])
        return description
    else:
        return "No labels detected for this image."
    
def extract_text_from_image(image_path):
    """
    Extracts text from the image at the given path using Google Cloud Vision API OCR.
    Returns the detected text as a string.
    """
    api_key = os.getenv("cloud_vision_api_key")
    if not api_key:
        raise Exception("cloud_vision_api_keymage not found. Make sure you have a .env file with the key.")

    client_options = ClientOptions(api_key=api_key)
    client = vision.ImageAnnotatorClient(client_options=client_options)

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Use text_detection for OCR
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    texts = response.text_annotations
    if texts:
        return texts[0].description  # The first item contains the full text
    else:
        return "No text detected in this image."

# Example usage: process all images in a directory and print their descriptions.
if __name__ == '__main__':
    # This should be the directory where your images were extracted.
    # It is based on the output from texteraction.py
    image_dir = "Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-08-02_BFS-.pdf_images"

    if not os.path.isdir(image_dir):
        print(f"Error: Image directory not found at '{image_dir}'")
        print("Please run texteraction.py first or update the image_dir variable.")
    else:
        print(f"Processing images in: {image_dir}")
        for filename in sorted(os.listdir(image_dir)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    full_path = os.path.join(image_dir, filename)
                    description = generate_image_description(full_path)
                    print(f"\n'{filename}':")
                    print(f"  {description}")
                except Exception as e:
                    print(f"\nCould not process '{filename}'. Error: {e}")
