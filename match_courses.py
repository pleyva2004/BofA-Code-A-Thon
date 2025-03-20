from agents import Agent, Runner
from agents import set_default_openai_key
from agents import set_tracing_export_api_key
import os
import csv

# set_default_openai_key(os.getenv("OPENAI_API_KEY"))
# set_tracing_export_api_key(os.getenv("TRACING_EXPORT_API_KEY"))


def match_courses(skill, courses):
    """
    Match courses to skills using a similarity search.
    
    Args:
        skills (list): List of skills to match
        courses (list): List of courses to match

    Returns:
        list: List of courses that match the skills
    """
    
    # Create a course matcher
    matcher = Agent(
        name="CourseMatcher",
        instructions="""
        You are a course matcher. Your task is to match the skills to the courses.

        You will be given a list a skill and a list of courses.
        You will need to match the skills to the courses.

        Input:
        - one long string where the first line is the skill and what follows is the courses.
        - the courses are formatted as title\ndescription\n\n

        Output:
        - a list of titles of the courses that match the skill.

        Please be very specific in your output and only return the titles of the courses that match the skill and small sample of the course description and why it matches the skill.

        """
    )

    # Run the matcher
    result = Runner.run_sync(matcher, input=f"Skill: {skill}\nCourses: {courses}")

    # Return the result
    return result.final_output
    

def process_courses(courses_csv):


    """
    Process the courses for matching.
    """
    # Read CSV file into list of courses
    courses = []
    with open(courses_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            courses.append(row)

    # Initialize empty string to store formatted course info
    formatted_courses = ""
    
    # Iterate through courses and format as title\ndescription\n\n
    for course in courses:
        title = course["title"]
        description = course["description"]
        formatted_courses += f"{title}\n{description}\n\n"
        
    return formatted_courses


    
if __name__ == "__main__":

    ai_engineer_skills = [
        "Python Programming",
        "Machine Learning Algorithms",
        "Deep Learning (CNNs, RNNs, Transformers)",
        "Data Structures & Algorithms",
        "Mathematics for AI (Linear Algebra, Calculus, Probability, Statistics)",
        "Model Training & Evaluation (Accuracy, Precision, Recall, F1-score)",
        "Data Preprocessing & Cleaning",
        "Natural Language Processing (NLP)",
        "Computer Vision",
        "AI Frameworks & Libraries (TensorFlow, PyTorch, Scikit-learn, Keras)",
        "Version Control (Git & GitHub)",
        "Cloud Platforms (AWS, GCP, Azure)",
        "Model Deployment (APIs, Flask/FastAPI, Docker)",
    ]

    for skill in ai_engineer_skills:
        # Process courses
        formatted_courses = process_courses("courses_courses.csv")

        # Match courses
        matched_courses =   match_courses(skill, formatted_courses)
        print(matched_courses + "\n\n") 

