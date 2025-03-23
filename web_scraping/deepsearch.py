import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re

logging.basicConfig(level=logging.INFO)

# Utility: get the HTML content of a URL (with requests, fallback to Selenium if needed)
def fetch_html(url, use_selenium=False):
    if not use_selenium:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}  # mimic a browser
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()  # raise an error for bad status codes
            return resp.text
        except Exception as e:
            logging.warning(f"Requests failed for {url}: {e}")
            return None
    else:
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            # Optionally, wait for dynamic content if needed:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            logging.error(f"Selenium failed for {url}: {e}")
            return None

def find_catalog_url(university_name):
    # Attempt heuristic patterns for common catalog URLs
    # e.g., "University of California, Berkeley" -> "berkeley.edu" + "/courses/compsci" or similar
    # For demo, we'll simulate this with a dictionary of known examples:
    known_catalogs = {
        "University of California, Berkeley": "https://guide.berkeley.edu/courses/compsci/",
        "The University of Texas at Austin": "https://catalog.utexas.edu/general-information/coursesatoz/c-s/", 
        # Additional known mappings can be added here...
    }
    if university_name in known_catalogs:
        return known_catalogs[university_name]
    # Fallback: do a web search (pseudo-code, as actual web search requires API or scraping Google)
    query = university_name + " computer science undergraduate courses"
    logging.info(f"Searching web for catalog page of {university_name} with query: {query}")
    # ... (search implementation or manual step) ...
    return None  # if not found


def parse_courses_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    courses_data = []
    # Strategy 1: look for course blocks by known HTML patterns
    # Example pattern: Heading tag (h3 or h4) followed by description in <p>
    for header in soup.find_all(['h3', 'h4', 'dt']):  # some catalogs use <dt> for course title in <dl>
        title_text = header.get_text(separator=" ", strip=True)
        # Heuristic: course title lines often contain course code and title
        if re.match(r'^[A-Z]{1,4}\s?\d+', title_text):  # starts with dept code and number
            # Find description: could be next sibling <p> or contained in <dd> if <dt>/<dd> structure
            desc = ""
            # Check next elements for description text
            next_node = header.find_next_sibling()
            if next_node and next_node.name in ['p', 'dd', 'div']:
                desc = next_node.get_text(" ", strip=True)
            courses_data.append((title_text, desc))
    return courses_data

def scrape_university_courses(university_name):
    logging.info(f"Starting scrape for {university_name}")
    url = find_catalog_url(university_name)
    if not url:
        logging.error(f"Catalog URL for {university_name} not found.")
        return None
    # Step 1: try to fetch with requests
    html = fetch_html(url, use_selenium=False)
    # Step 2: if requests failed or returned nothing, try Selenium
    if html is None or len(html) < 1000:  # if content is too short, maybe it didn't load
        logging.info(f"Retrying {university_name} with Selenium.")
        html = fetch_html(url, use_selenium=True)
        if html is None:
            logging.error(f"Failed to retrieve content for {university_name}")
            return None
    # Step 3: parse the HTML for courses
    courses = parse_courses_from_html(html)
    if not courses:
        logging.warning(f"No courses found for {university_name} (parser might need an update).")
    else:
        logging.info(f"Found {len(courses)} courses for {university_name}.")
    return courses

# Example usage:
university_list = [
    "University of California, Berkeley",
    "The University of Texas at Austin"
]
for uni in university_list:
    course_list = scrape_university_courses(uni)
    if course_list:
        # Print first 2 courses as a sample output
        for c in course_list[:2]:
            print(f"{uni} - {c[0]} : {c[1][:60]}...")
        print("...")  # indicate output truncated


def main():
    university_list = [
        "New Jersey Institute of Technology ",
        "University of Texas, Arlington",
        
    ]
    for uni in university_list:
        course_list = scrape_university_courses(uni)
        if course_list:
            # Print first 2 courses as a sample output
            for c in course_list[:2]:
                print(f"{uni} - {c[0]} : {c[1][:60]}...")
            print("...")  # indicate output truncated

if __name__ == "__main__":
    main()

