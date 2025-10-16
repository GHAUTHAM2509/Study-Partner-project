import os
import requests
import logging
import base64
import json
from dotenv import load_dotenv
import google.auth
from google.auth.transport.requests import Request

# Load environment variables from .env file
load_dotenv()

# The endpoint for your Document AI processor
document_endpoint="https://eu-documentai.googleapis.com/v1/projects/178535507469/locations/eu/processors/13f9c98412bc04f1/processorVersions/pretrained-foundation-model-v1.5-pro-2025-06-20:process"

def process_pdf_with_docai(pdf_content: bytes, mime_type: str = "application/pdf"):
    """
    Sends a PDF to the specified Google Document AI endpoint for processing using OAuth2.

    Args:
        pdf_content: The raw byte content of the PDF file.
        mime_type: The MIME type of the file (default is "application/pdf").

    Returns:
        dict: The JSON response from the Document AI API.
              Returns None if an error occurs.
    """
    try:
        # 1. Get Application Default Credentials and create an access token
        logging.info("Fetching authentication credentials...")
        credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        auth_req = Request()
        credentials.refresh(auth_req)
        access_token = credentials.token
        logging.info("Successfully fetched access token.")

        # 2. Prepare the request headers with the OAuth2 token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        # 3. Encode the PDF content in base64
        encoded_content = base64.b64encode(pdf_content).decode("utf-8")

        # 4. Construct the JSON request body
        data = {
            "rawDocument": {
                "content": encoded_content,
                "mimeType": mime_type,
            }
        }

        # 5. Make the POST request to the Document AI endpoint
        logging.info("Sending request to Document AI endpoint...")
        # Note: The URL does not contain the API key anymore
        response = requests.post(document_endpoint, headers=headers, json=data)
        
        response.raise_for_status()
        
        logging.info("Successfully processed document.")
        return response.json()

    except google.auth.exceptions.DefaultCredentialsError:
        logging.error("Authentication failed. Please run 'gcloud auth application-default login'")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Document AI failed: {e}")
        if e.response is not None:
            logging.error(f"API Response: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def retrieve_questions_from_paper(paper_link: str):
    """
    Retrieves questions from a given paper using Document AI.

    Args:
        paper_link: The URL of the paper to analyze.

    Returns:
        list: A list of questions extracted from the paper.
    """
    try:
        logging.info(f"Retrieving questions from paper: {paper_link}")
        # Download the PDF content from the paper link
        pdf_response = requests.get(paper_link)
        pdf_response.raise_for_status()
        pdf_bytes = pdf_response.content

        # Process the PDF using Document AI
        result = process_pdf_with_docai(pdf_bytes)

        if result:
            questions = []
            for entity in result.get('document', {}).get('entities', []):
                questions.append(entity.get('mentionText', ''))
            return questions
        else:
            logging.error("Failed to get result from Document AI.")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download PDF: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the main execution: {e}")

# --- Example Usage ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # The PDF is hosted at this URL
    pdf_url = 'https://storage.googleapis.com/papers-codechefvit-prod/papers/bcw1uk69ucsuao4cq5fd.pdf'
    
    try:
        logging.info(f"Downloading PDF from {pdf_url}")
        # Download the PDF content from the URL
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()
        pdf_bytes = pdf_response.content
        logging.info("PDF downloaded successfully.")

        # Process the PDF using Document AI
        result = process_pdf_with_docai(pdf_bytes)

        if result:
            document_text = []
            for entity in result.get('document', {}).get('entities', []):
                document_text.append(entity.get('mentionText', ''))
            print("\n--- Document AI Response ---")
            print(document_text)
            # To see the full structure, you can save it to a file
            # with open('doc_ai_response.json', 'w') as f:
            #     json.dump(result, f, indent=2)
            # logging.info("Full response saved to doc_ai_response.json")
        else:
            logging.error("Failed to get result from Document AI.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download PDF: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the main execution: {e}")

