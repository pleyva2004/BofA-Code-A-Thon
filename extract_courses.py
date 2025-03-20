import requests
from agents import Agent, Runner
from agents import set_default_openai_key
from agents import set_tracing_export_api_key
from bs4 import BeautifulSoup
import csv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_api_keys(openai_key=None):
    """Configure API keys for the scraper"""
    if openai_key:
        set_default_openai_key(openai_key)
        set_tracing_export_api_key(openai_key)
    elif os.getenv("OPENAI_API_KEY"):
        set_default_openai_key(os.getenv("OPENAI_API_KEY"))
        set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError("OpenAI API key must be provided either as argument or environment variable")

def paragraph_classifier(text):
    """Classify if the text is a course description"""
    logger.debug("Classifying paragraph")
    
    description_classifier = Agent(name="Assistant", instructions="""
                    You are a description classifier. Your task is to analyze the provided text and decide if the text is the description of the given title course or not.

                    If the text is not a description, return "False".
                    If the text is a description, return the description.
                    """)
                             
    description_result = Runner.run_sync(description_classifier, text)
    return description_result.final_output

def scrape_courses(url, openai_key=None):
    """
    Scrape course information from a university catalog page.
    
    Args:
        url (str): The URL of the catalog page to scrape
        openai_key (str, optional): OpenAI API key. If not provided, will look for environment variable
    
    Returns:
        list: List of dictionaries containing course information
    """
    try:
        # Configure API keys if needed
        configure_api_keys(openai_key)
        
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        courses_section = soup.find_all('p')
        courses = []

        # Process each paragraph
        i = 0
        while i < len(courses_section):
            logger.debug(f"Processing paragraph {i}")
            text = courses_section[i].get_text().strip()
            
            course_classifier = Agent(name="Assistant", instructions="""
                    You are a course Classifying Specialist. Your task is to analyze the provided text and decide if the text is the title of a course or not.

                    If the course is not a title, return "False".
                    If the course is a title, return the course title - make sure to include the course code in the course title.
                    """)
            
            course_result = Runner.run_sync(course_classifier, text)

            if course_result.final_output != "False":
                title = course_result.final_output
                logger.info(f"Found course: {title}")

                # Look for description in subsequent paragraphs
                j = i
                description = paragraph_classifier(text)
                while description == "False" and j < len(courses_section) - 1:
                    j += 1
                    text = courses_section[j].get_text().strip()
                    description = paragraph_classifier(text)
                
                if description != "False":
                    course = {
                        "title": title,
                        "description": description
                    }
                    if not any(c["title"] == title for c in courses):
                        courses.append(course)
                        logger.info(f"Added course: {title}")
                    i = j
                
            i += 1
        
        return courses
        
    except requests.RequestException as e:
        logger.error(f"Error fetching webpage: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
        raise

def save_to_csv(courses, filename):
    """Save courses to CSV file"""
    if not courses:
        logger.warning("No courses to save")
        return
        
    try:
        fields = courses[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(courses)
        logger.info(f"Successfully saved {len(courses)} courses to {filename}")
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
        raise

def clean_url(url):
    """Extract university name from URL"""
    clean_url = url.replace('https://', '').replace('http://', '')
    parts = clean_url.split('.')
    return parts[1].upper()

# Example usage
if __name__ == "__main__":
    URLS = {
        "MIT": "https://student.mit.edu/catalog/m6a.html",
        "NJIT": "https://catalog.njit.edu/undergraduate/computing-sciences/computer-science/#coursestext",
        "HARVARD": "https://www.seas.harvard.edu/computer-science/courses"
    }
    
    try:
        # Example: scrape MIT courses
        courses = scrape_courses(URLS["MIT"])
        if courses:
            filename = f"MIT_courses.csv"
            save_to_csv(courses, filename)
    except Exception as e:
        logger.error(f"Failed to scrape courses: {e}")




