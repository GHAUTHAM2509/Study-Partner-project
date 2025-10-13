import sys, pathlib, pymupdf, os
from texteractionpdf import extract_text_and_images_from_pdf
from imagedescription import generate_image_description, extract_text_from_image
# extract_text_and_images_from_pdf("tempdoc1.pdf")
print(generate_image_description("tempdoc1.pdf_images/image_32_1.jpeg"))
print(extract_text_from_image("tempdoc1.pdf_images/image_32_1.jpeg"))