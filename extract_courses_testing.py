import requests
from agents import Agent, Runner
from agents import set_default_openai_key
from agents import set_tracing_export_api_key
from bs4 import BeautifulSoup
import csv
import os

set_default_openai_key(os.getenv("OPENAI_API_KEY"))
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))


def paragraph_classifier(text):
    """Classify the paragraph"""

    print("inside paragraph classifier")

    description_classifier = Agent(name="Assistant", instructions="""
                        You are a description classifier. Your task is to analyze the provided text and decide if the text is the description of the given title course or not= course or not.

                        If the text is not a description, return "False".
                        If the text is a description, return the description.
                        """)
                                 
    description_result = Runner.run_sync(description_classifier, text)

    return description_result.final_output

def scrape_courses(url):
    """
    Scrape course information from catalog page.
    """
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the courses section
        courses_section = soup.find_all('p')
        print(courses_section)
        
        courses = []


        
        # Process each paragraph
        i = 0
        while i < len(courses_section):
            print("i: ", i)
            text = courses_section[i].get_text().strip()
            print(text)
            course_classifier = Agent(name="Assistant", instructions="""
                        You are a course Classifying Specialist . Your task is to analyze the provided text and decide if the text is the title of a course or not.

                        If the course is not a title, return "False".
                        If the course is a title, return the course title  make sure to include, MAKE SURE TO INCLUDE the course code in the course title.
                           

                                      
                        Please process the following text and provide the structured output:""")
            course_result = Runner.run_sync(course_classifier, text)


            if course_result.final_output != "False":
                title = course_result.final_output
                print("--------------------------------")
                print(title)
                print("--------------------------------")



                # call paragraph classifier
                print("Classifying Description")
                print("--------------------------------")
                print(text)
                description = paragraph_classifier(text)
                print(description)
                j = i
                while description == "False":
                    j = j + 1
                    text = courses_section[j].get_text().strip()
                    print("Describtion not found, trying again")
                    print("j: ", j)
                    print(text)
                    description = paragraph_classifier(text)
                    print(description)
                    print("--------------------------------")
                
                print("--------------------------------")
                print(description)
                print("--------------------------------")

                i = j
                print("i: ", i)
        
                course = {
                    "title": title,
                    "description": description
                }

                if title not in courses:
                    courses.append(course)
                    print("--------------------------------")
                    print(course)
                    print("--------------------------------")
            i += 1  # Manual increment when we didn't jump
        
        return courses
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def save_to_csv(courses, filename):
    """Save courses to CSV file"""
    
    if not courses:
        return
        
    fields = courses[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(courses)

def clean_url(url):
    clean_url = url.replace('https://', '').replace('http://', '')
    parts = clean_url.split('.')
    return parts[1].upper()


def main():
    url_mit = "https://student.mit.edu/catalog/m6a.html"
    url_njit = "https://catalog.njit.edu/undergraduate/computing-sciences/computer-science/#coursestext"
    url_harvard = "https://www.seas.harvard.edu/computer-science/courses"
    url_berkeley = "https://www2.eecs.berkeley.edu/Courses/CS/"

    
    courses = scrape_courses(url_njit)
    filename = f"{clean_url(url_njit)}_courses.csv"


    if courses:
        print(f"Successfully extracted {len(courses)} courses")
        # save_to_json(courses)
        save_to_csv(courses, filename)
        print(f"Data saved to {filename}")
    else:
        print("No courses were extracted")

if __name__ == "__main__":
    main()




