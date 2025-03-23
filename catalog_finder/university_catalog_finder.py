import requests
from bs4 import BeautifulSoup
import re

def search_university_catalog(university_name):
    """
    Search for a university's computer science course catalog URL.
    Args:
        university_name (str): Name of the university
    Returns:
        str: URL of the computer science course catalog if found, None otherwise
    """
    # Format the search query
    search_query = f"{university_name} computer science course catalog"
    
    try:
        # Use OpenAI's GPT-4 with web search
        from openai import OpenAI
        client = OpenAI()
        
        # Perform web search using chat completion
        completion = client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that finds computer science course catalog URLs. Return only the URL if found, or 'None' if not found."
                },
                {
                    "role": "user",
                    "content": f"Find the computer science course catalog URL for {university_name}. Only return the URL or 'None'."
                }
            ],
            web_search_options={}
        )
        
        # Extract URL from response
        result = completion.choices[0].message.content.strip()
        
        # Verify if the result is a valid URL
        if result.lower() == 'none':
            return None
            
        # Additional verification for the URL
        if any(keyword in result.lower() for keyword in ['catalog', 'courses', 'curriculum', 'bulletin']) and \
           ('.edu' in result or any(domain in result for domain in ['university', 'college', 'institute'])):
            
            # Try to find more specific course listing sections
            course_sections = ['#coursestext', '#courses', '#course-list', '#course-descriptions']
            base_url = result.split('#')[0]
            
            # If URL doesn't end with a course section, try to append one
            if not any(result.endswith(section) for section in course_sections):
                return base_url
            return result
                
        return None
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    while True:
        # Get university name from user
        university_name = input("\nEnter university name (or 'quit' to exit): ")
        
        if university_name.lower() == 'quit':
            break
            
        # Search for the catalog
        print(f"\nSearching for {university_name}'s computer science course catalog...")
        catalog_url = search_university_catalog(university_name)
        
        if catalog_url:
            print(f"\nFound course catalog URL: {catalog_url}")
        else:
            print("\nCould not find the course catalog. Please try a different university name or check your spelling.")

if __name__ == "__main__":
    print("Welcome to the University CS Catalog Finder!")
    print("This program helps you find computer science course catalogs for universities.")
    print("\nNote: This program requires an OpenAI API key to be set in your environment.")
    print("Please set the OPENAI_API_KEY environment variable before running.")
    main() 