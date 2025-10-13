# This script provides batch processing for PDF and PPTX files in specified directories.
# It uses texteractionpdf.py and texteractionppt.py to extract text and images from files.

from pptx import Presentation
import os,  pathlib, sys, pymupdf
from time import sleep
from texteractionppt import extract_text_from_pptx
from texteractionpdf import extract_text_and_images_from_pdf

def process_pdf_files(pdf_dir):
    """
    Processes all PDF files in the given directory using extract_text_and_images_from_pdf.
    """
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"Processing {pdf_path}...")
            extract_text_and_images_from_pdf(pdf_path)
            print(f"Finished processing {pdf_path}.")

def process_pptx_files(pptx_dir):
    """
    Processes all PPTX files in the given directory using extract_text_from_pptx.
    """
    for filename in os.listdir(pptx_dir):
        if filename.endswith(".pptx"):
            pptx_path = os.path.join(pptx_dir, filename)
            print(f"Processing {pptx_path}...")
            extract_text_from_pptx(pptx_path)
            print(f"Finished processing {pptx_path}.")

# Example usage: process all PDFs and PPTXs in their respective directories.
if __name__ == "__main__":
    pdf_dir = '../Data/aws'  # The path is relative to this script's location (backend/Preprocessing)
    process_pdf_files(pdf_dir)
    # pptx_dir = 'Data/ppts'
    # process_pptx_files(pptx_dir)
