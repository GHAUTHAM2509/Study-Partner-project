#boiler plate for a python script for scapping a website
import re
import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def scrape_website(url):
    """
    Scrapes a website using Selenium to handle dynamic content.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Add a more common user-agent to avoid being blocked
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = None  # Initialize driver to None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        # Wait for a specific, unique element that indicates content is loaded.
        # Let's wait for the container that holds all the paper cards.
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid.grid-cols-1"))
        )
        
        # Give it an extra moment for any final rendering
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Save the output for debugging
        # with open("debug_output.html", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())
            
        driver.quit()
        return soup
    except Exception as e:
        logging.error(f"Error fetching {url} with Selenium: {e}")
        if driver:
            driver.quit()
        return None

def extract_paper_info(soup):
    """
    Extracts information about each paper from the scraped website.
    """
    if not soup:
        return []

    # Use a more reliable CSS selector to find the paper containers.
    # This looks for a div that has both 'overflow-hidden' and 'border-2' classes.
    paper_containers = soup.select('div.overflow-hidden.border-2')
    
    extracted_data = []

    for container in paper_containers:
        paper_info = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Find the main link for the paper
        link_tag = container.find('a', href=True)
        if link_tag:
            base_url = "https://papers.codechefvit.com"
            paper_info['link'] = base_url + link_tag['href']
            page_response = requests.get(paper_info['link'], headers=headers)
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
            if pdf_url:
                paper_info['pdf_link'] = pdf_url
        # Find the course code (e.g., BCSE303L)
        code_tag = container.find('div', class_='text-md font-play font-medium')
        if code_tag:
            paper_info['course_code'] = code_tag.get_text(strip=True)

        # Find the course title (e.g., Operating Systems)
        title_tag = container.find('div', class_='font-play text-lg font-semibold')
        if title_tag:
            paper_info['title'] = title_tag.get_text(strip=True)
            
        # Find all the tags (e.g., CAT-1, 2023-2024, etc.)
        tags_container = container.find('div', class_='flex flex-wrap gap-2')
        if tags_container:
            tags = tags_container.find_all('div')
            paper_info['tags'] = [tag.get_text(strip=True) for tag in tags]
        
        if paper_info:
            extracted_data.append(paper_info)
            
    return extracted_data

url = "https://papers.codechefvit.com/catalogue?subject=operating%20systems"
soup = scrape_website(url)
papers = extract_paper_info(soup)
#print(papers)
# Pretty print the extracted data
#print(json.dumps(papers, indent=2))