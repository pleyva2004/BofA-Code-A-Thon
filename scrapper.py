from scrapegraphai.graphs import SmartScraperGraph
import json
import os

def scrape_courses(url):
    print("Starting to scrape courses")
    graph_config = {
        "llm": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "openai/gpt-4o-mini",
            "temperature":0,
        },
        "verbose":True,
        "format": "json",

    }

    # ************************************************
    # Create the SmartScraperGraph instance and run it
    # ************************************************

    smart_scraper_graph = SmartScraperGraph(
        prompt="Extract every undergraduate Computer Science course with course name , course code, please include the course code in the course name, and description from the given link",
        source=url,
        config=graph_config
    )

    result = smart_scraper_graph.run()

    output = json.dumps(result, indent=2)

    return output


if __name__ == "__main__":
    url = "https://catalog.uta.edu/coursedescriptions/cse/"
    courses = scrape_courses(url)
    print(courses)
