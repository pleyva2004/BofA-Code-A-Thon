import requests
import os

#Hard Coded School name, needs to be retrieved from the FE/BE later on
school_name = 'New Jersey Institte of Technology'
#This is temporary, as it is not as effective as I would like for all colleges
#Edit the search query as you please
search_query = school_name + ' site:.edu ("computer science" OR "cs" OR "course descriptions")'

def get_cs_courses(api_key):
    # Set up the parameters for the search.
    params = {
        "engine": "google",
        "q": search_query,
        "api_key": api_key,
        "hl": "en",  # language
        "gl": "us"   # location, adjust if needed
    }
    # Send a GET request to the SerpApi endpoint.
    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()  # Raises an error for unsuccessful requests.
    return response.json()

def parse_courses(results):
    courses = []
    # Extract data from the organic search results.
    # Note: The structure of the results may vary. Adjust parsing as needed.
    for result in results.get("organic_results", []):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        courses.append({
            "title": title,
            "snippet": snippet,
            "link": link #all we need is the link, maybe title
        })
    return courses

def main():
    # Load environment variables
    api_key = os.getenv("SERP_API_KEY")
    
    if not api_key:
        raise ValueError("SERP_API_KEY not found in environment variables")
    
    try:
        results = get_cs_courses(api_key)
        courses = parse_courses(results)
        
        print(search_query + " (Search Results):\n")
        for course in courses:
            print(f"Title: {course['title']}")
            print(f"Snippet: {course['snippet']}")
            print(f"Link: {course['link']}")
            print("-" * 40)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()