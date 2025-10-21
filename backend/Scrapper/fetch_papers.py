import requests
import logging
import json

def fetch_papers_from_api(subject):
    """
    Fetches paper information directly from the CodeChef VIT Papers API.
    """
    # The API expects subject names to be URL-encoded (e.g., "Operating Systems" -> "Operating%20Systems")
    # The requests library handles this automatically, so no need for manual replacement.
    url = "https://papers.codechefvit.com/api/papers"
    params = {'subject': subject}
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        logging.info(f"Fetching papers for subject: {subject} from API")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        
        # The API might return a dictionary like {'papers': [...]}.
        # We need to get the list from the 'papers' key.
        papers_list = data.get('papers', []) if isinstance(data, dict) else data
        
        papers = []

        for item in papers_list:
            # Ensure the item has a unique identifier before processing.
            paper_id = item.get("_id")
            if not paper_id:
                logging.warning(f"Skipping paper due to missing '_id': {item}")
                continue

            # Construct the full paper detail page link from the slug
            link = f"https://papers.codechefvit.com/paper/{paper_id}"

            paper_info = {
                "id": paper_id,
                "subject": item.get("subject", "N/A"),
                "tags": [tag for tag in [item.get('exam'), item.get('year'), item.get('slot'), item.get('semester')] if tag],
                "link": link,
                "pdf_link": item.get("file_url") # The API provides the direct PDF link
            }
            papers.append(paper_info)
        
        logging.info(f"Fetched {len(papers)} papers successfully from API.")
        return papers

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return []
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from API response.")
        return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    subject_to_test = "Operating Systems"
    papers_data = fetch_papers_from_api(subject_to_test)
    print(json.dumps(papers_data, indent=2, ensure_ascii=False))
