import requests
import logging
from google.cloud import vision
from bs4 import BeautifulSoup
import re

def extract_text_from_pdf_with_vision(paper_page_url):
    """
    Scrapes a paper's HTML page to find the direct PDF URL, then downloads
    the PDF and uses Google Cloud Vision to extract its text.

    Args:
        paper_page_url (str): The URL of the paper's web page (e.g., .../paper/{id}).

    Returns:
        str: The extracted text from the PDF, or None if an error occurs.
    """
    try:
        # 1. Scrape the page to find the actual PDF URL from the script tag
        logging.info(f"Scraping page to find PDF URL: {paper_page_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page_response = requests.get(paper_page_url, headers=headers)
        page_response.raise_for_status()
        
        soup = BeautifulSoup(page_response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        pdf_url = None
        # Regex to find Google Storage URLs for PDFs
        url_pattern = re.compile(r'https://storage\.googleapis\.com/.*?\.pdf')

        for script in scripts:
            if script.string:
                match = url_pattern.search(script.string)
                if match:
                    pdf_url = match.group(0)
                    logging.info(f"Found PDF URL: {pdf_url}")
                    break
        
        if not pdf_url:
            logging.error("Could not find PDF URL in the page scripts.")
            return None

        # 2. Download the PDF content from the found URL
        logging.info(f"Downloading PDF from {pdf_url}")
        pdf_response = requests.get(pdf_url, headers=headers)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        print(pdf_content, pdf_url)
        logging.info("PDF downloaded successfully.")

        # 3. Use Google Cloud Vision to extract text
        # client = vision.ImageAnnotatorClient()
        # input_config = vision.InputConfig(content=pdf_content, mime_type='application/pdf')
        # features = [vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)]
        
        # # Process up to 5 pages for synchronous requests.
        # request = vision.AnnotateFileRequest(
        #     input_config=input_config, features=features, pages=[1, 2, 3, 4, 5]
        # )

        # logging.info("Sending request to Google Cloud Vision API...")
        # response = client.batch_annotate_files(requests=[request])
        
        # full_text = ""
        # for image_response in response.responses[0].responses:
        #     full_text += image_response.full_text_annotation.text

        # logging.info("Text extracted successfully.")
        # return full_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during network request: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred with Google Cloud Vision or parsing: {e}")
        return None

# --- Example Usage ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # This is the HTML page URL for the paper
    paper_page_url = "https://papers.codechefvit.com/paper/6891c293f6766a56a03f5c05"
    
    extracted_text = extract_text_from_pdf_with_vision(paper_page_url)
    
    if extracted_text:
        print("\n--- Extracted Text (first 1000 characters) ---")
        print(extracted_text[:1000])
    else:
        print("\n--- Failed to extract text. ---")