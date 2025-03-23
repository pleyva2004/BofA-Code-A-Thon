from scrapper import scrape_courses
import csv
import json
from match_courses import process_courses, match_courses
import pandas as pd

def export_json_to_csv_pandas(json_data, csv_filename):
    """
    Export JSON data to CSV file using pandas.
    
    Args:
        json_data (list): List of dictionaries or complex JSON object
        csv_filename (str): Name of the output CSV file
    """
    # Convert JSON to DataFrame
    df = pd.DataFrame(json_data)
    
    # Export to CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8')

def main(target_url, career):
    
    # Example URL - replace with your target university's course catalog URL
    # target_url = "https://cea.howard.edu/cs-course-descriptions"
    
    
    # Call the scrape_courses function
    courses = scrape_courses(target_url)

    json_courses = json.loads(courses)

    modified_json_courses = json_courses['content']

    # Define CSV filename
    csv_filename = "courses_courses.csv"
    
    # Export JSON data to CSV
    export_json_to_csv_pandas(modified_json_courses, csv_filename)

    # Process courses from the CSV file
    formatted_courses = process_courses(csv_filename)

    print(f"\nMatching courses to {career} skills...")
    print("=" * 50)

    ai_engineer_skills = [
        "AI",
        "Machine Learning",
        "Deep Learning",
        "Computer Vision",
        "Natural Language Processing",
        "Reinforcement Learning",
        "Generative AI",
        "Prompt Engineering",
        "LLMs",
        "NLP",
        "CV",
        "RL",
        "Generative AI",
        "Prompt Engineering",
        "LLMs"
    ]
    
    Frontend_Engineer = [
        "HTML",
        "CSS",
        "JavaScript",   
        "React",
        "UI/UX Design",
        "Responsive Design",
        "DOM Manipulation",
        "React Components",
        "UI Kits",
        "Event Handling",
        "Arrays",
        "Strings",
        "RESTful APIs",
        "Authentication",
        "Data Structures"
        ]
    
 
    Backend_Engineer = [
        "Python",
        "Django",
        "Flask",
        "Express",
        "Node.js",
    ]

    Data_Scientist = [
        "Python",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "SQL",
        "NoSQL",
        "Statistics",
        "Machine Learning",
    ]

    Cyber_Security_Engineer = [
        "Cybersecurity",
        "Network Security",
        "Web Security",
        "Cloud Security",
        "Cybersecurity",
        "Ethical Hacking",
        "Cryptography",
    ]

    Game_Developer = [
        "Game Development",
        "Unity",
        "Unreal Engine",
        "Game Design",
        "Game Programming",
        "C#",
        "Game Physics",
    ]


    if career == "AI Engineer":
        skills = ai_engineer_skills
    elif career == "Frontend Engineer":
        skills = Frontend_Engineer
    elif career == "Backend Engineer":
       skills = Backend_Engineer
    elif career == "Data Scientist":
       skills = Data_Scientist
    elif career == "Cyber Security Engineer":
       skills = Cyber_Security_Engineer
    elif career == "Game Developer":
       skills = Game_Developer
    else:
        raise ValueError("Invalid career choice. Please choose from available careers.")

    # Match each skill to relevant courses
    matched_courses = match_courses(skills, formatted_courses)
    output = f"\n{career}\n" + "-" * 30 + "\n" + matched_courses
    print(output)
    print(f"Courses saved to {csv_filename}")
    
    return output



if __name__ == "__main__":
    main()
