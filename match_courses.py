from agents import Agent, Runner
from agents import set_default_openai_key
from agents import set_tracing_export_api_key
import os
import csv
import asyncio


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

        Example:
            input: 

            Skills: ["AI", "Machine Learning", "Deep Learning", "Computer Vision", "Natural Language Processing", "Reinforcement Learning", "Generative AI", "Prompt Engineering", "LLMs", "NLP", "CV", "RL", "Generative AI", "Prompt Engineering", "LLMs"]

            Courses:
            course_name,description
            Programming for Bioinformatics,The ability to use existing programs and to write small programs to access bioinformatics information or to combine and manipulate various existing bioinformatics programs has become a valuable part of the skill set of anyone working with biomolecular or genetic data. This course provides an understanding of the architecture of bioinformatics toolkits and experience in writing small bioinformatics programs using one or more of the scripting ('glue') languages frequently employed for such tasks.
            Computer Programming and Problem Solving,"An introductory course that is designed for engineering freshmen. This course introduces students to the engineering problem solving process in the context of MATLAB. The emphasis is on the logical analysis of a problem and the formulation of a computer program leading to its solution. Topics include basic concepts of computer systems, algorithm design, programming languages and data abstraction. At the end of class, a comparison between MATLAB and C/C++ will be discussed to provide students a better understanding of the general concept of computer programming."
            Computer Science with Business Problems,"An introductory course in computer science, with applications to business and managerial decision making. Topics include basic concepts of computer systems, software engineering, algorithm design, programming languages and abstraction, with applications."
            Computer Programming and Graphics Problems,"An introductory course in computer science with applications in computer graphics for architecture. Emphasis on programming methodology using a high level language as the vehicle to illustrate the concepts. Topics include basic concepts of computer systems, software engineering, algorithm design, programming languages and data abstraction, with applications."
            Introduction to Computing,"An introduction to programming and problem solving skills for non-computing majors using Python programming languages. Topics include basic strategies for problem solving, constructs that control the flow execution of a program and the use of high level data types such as lists, strings, and dictionaries in problem representation. The course also presents an overview of selected 'big idea' topics in computing."
            Introduction to Computer Science I,"Intensive introduction to computer science. Problem solving decomposition. Writing, debugging, and analyzing computer programs. Introduction to arrays and lists. Iteration and recursion. The Java language is introduced and used to highlight these concepts."
            Introduction to Computer Science II,"A study of advanced programming topics with logical structures of data, their physical representation, and the design of computer algorithms operating on the structures. Course covers program specifications, correctness and efficiency, data abstraction, and algorithm analysis."
            Introduction to Computer Science I in C++,"Fundamentals of computer science are introduced, with emphasis on programming methodology and problem solving. Topics include basic concepts of computer systems, software engineering, algorithm design, programming languages and data abstraction, with applications."
            Introduction to Computer Science II in C++,"A study of advanced programming topics with logical structures of data, their physical representation, design and analysis of computer algorithms operating on the structures, and techniques for program development and debugging."
            Technical History of Computing,"This course is for students in computing majors. Students will gain a comprehensive overview of the evolution of computing from the start of recorded history through modern times. By studying history, you will understand the context of modern developments in CS/IT, including cyclical trends and why various approaches did or did not work."
            Foundations of Computer Science I,An introduction to the foundations of computer science with emphasis on the development of techniques for the design and proof of correctness of algorithms and the analysis of their computational complexity.
            Game Modification Development,"This course introduces students to the basic concepts of game programming and development. Students will learn how to reprogram a professional game engine, or Modification (Mod) development as it is referred to in the industry."
            2D Game Development,This course introduces students to the core concepts and skills necessary for the development of games utilizing 2D graphics. Students will learn how to set up and program their own 2D graphics based game engine.
            Programming Language Concepts,"Conceptual study of programming language syntax, semantics and implementation. Course covers language definition structure, data types and structures, control structures and data flow, run-time consideration, and interpretative languages."
            Intensive Programming in Linux,"The course covers Linux programming with Apache Web and MySql database using Php/Python and C as primary languages. It consists of four stages: basic tools such as Bash and C programming; searching trees and matrix computing, end-to-end applications such as one that constantly presents top 100 stocks; and extending the applications to run on multiple machines."
            Introduction to Data Science,This course is designed for CS BS students to equip them with introductory principles as well as hands-on skills that are required to solve data science problems.
            Database System Design & Mgmt,"Database system architecture; data modeling using the entity-relationship model; storage of databases; the hierarchical, network and relational data models; formal and commercial query languages; functional dependencies and normalization for relational database design."
            Principles of Operating Systems,"Organization of operating systems covering structure, process management and scheduling; interaction of concurrent processes; interrupts; I/O, device handling; memory and virtual memory management and file management."
            Introduction to UNIX Operating Systems,"The course covers the UNIX system kernel including initialization, scheduling, context switching, process management, memory management, device management, and the file system."
            Performance Modeling in Computing,"Introduction to probability models and techniques useful in computer science. Performance evaluation, discrete-event simulation, classification and optimization are covered."
            Foundations of Computer Science II,"This course provides an introduction to automata theory, computability theory, and complexity theory."
            Intro to Computer Systems,"An introduction to the organization and architecture of computer systems, including the standard Von Neumann model and more recent architectural concepts."
            Introduction to Cybersecurity,"This course will give a broad overview of cybersecurity. There are two main goals of this course. First, students will learn fundamental concepts of cybersecurity."
            Introduction to Computer Networks,"This course provides an introduction to computer networks, with a special focus on Internet architecture and protocols."
            Fundamentals of Network Security,"This course offers an in-depth study of network security issues, types of computer and network attacks, and effective defenses."
            3D Game Development,This course introduces students to the core concepts and skills necessary for the development of games utilizing 3D graphics.
            Introduction to Artificial Intelligence,"This course addresses the theoretical foundation, methodologies, and applications of AI."
            Introduction to Machine Learning,"This is an introductory course to Machine Learning (ML). It consists of: (i) A smooth, example-based presentation of the fundamental notions of ML via simple algorithms and visualizable 'toy' data sets."
            Android Application Development,This course introduces mobile application development for the Android platform.
            Cryptography and Internet Security,Covers security requirements for telecommunication over the Internet and other communication networks.
            Introduction to Linux Kernel Programming,An introductory study of how the Linux operating system is built from scratch.
            Advanced Database Systems,"The course covers the basic concepts of traditional files and file processing, provides a 'classic' introduction to the relational data model and its languages."
            Advanced Data Structures and Algorithm Design,"Advanced topics in data structures and algorithms, involving sequences, sets, and graphs."
            Interactive Computer Graphics,This course introduces fundamental concepts of interactive graphics oriented toward computer-aided design systems.
            Image Processing and Analysis,"This course is an intensive study of the fundamentals of image processing, analysis and understanding."
            Computer Vision,This course introduces basic concepts and methodologies of computer vision.
            Big Data Systems,"This course provides a broad coverage of topics on big data generation, transfer, storage, management, computing, and analytics."
            Data Visualization,"The course provides students an introduction to computer graphics and the knowledge for designing, developing, and applying techniques for both information and volume visualization."
            Technologies-Network Security,This course provides both an in-depth theoretical study and a practical exposure to technologies that are critical in providing secure communication over the Internet.
            Data Mining,The course covers the concepts and principles of advanced data mining systems design.
            Selected Topics In CS,The study of new and/or advanced topics in an area of computer science not regularly covered in any other CS course.
            Independent Study in Computer Science,"Independent studies, investigations, research, and reports on advanced topics in computer science."
            Computer Science Research Project,This course is for students who have completed an independent study course and wish to delve deeper into research.
            Guided Design in Software Engineering,This course focuses on the methodology for developing software systems.
            Senior Project,An opportunity for the student to integrate the knowledge and skills gained in previous computer science work into a team-based project.
            Data Science Capstone I,The Data Science (DS) Capstone Project spans two semesters and is intended to provide a real-world project-based learning experience for seniors in the BS DS program.
            Data Science Capstone II,The Data Science (DS) Capstone Project spans two semesters and is intended to provide a real-world project-based learning experience for seniors in the BS DS program.

            output:
            1. **Introduction to Artificial Intelligence**
            - *Sample Description:* This course addresses the theoretical foundation, methodologies, and applications of AI.
            - *Why it matches:* Directly related to "AI" as it covers AI methodologies and applications.

            2. **Introduction to Machine Learning**
            - *Sample Description:* A smooth, example-based presentation of the fundamental notions of ML.
            - *Why it matches:* Focuses on "Machine Learning" concepts and methodologies.

            3. **Computer Vision**
            - *Sample Description:* Introduces basic concepts and methodologies of computer vision.
            - *Why it matches:* Specifically targeted towards "Computer Vision" skills.

            4. **Image Processing and Analysis**
            - *Sample Description:* Intensive study of the fundamentals of image processing, analysis and understanding.
            - *Why it matches:* Directly relevant to "Computer Vision" and related analysis techniques.

            5. **Introduction to Data Science**
            - *Sample Description:* Equips students with skills required to solve data science problems.
            - *Why it matches:* Includes topics that might intersect with "Machine Learning" and "NLP" skills.

            6. **Big Data Systems**
            - *Sample Description:* Broad coverage of topics on big data generation and analytics.
            - *Why it matches:* Supports skills related to "Machine Learning" through data handling and analytics.

            7. **Data Mining**
            - *Sample Description:* Concepts and principles of advanced data mining systems design.
            - *Why it matches:* Relevant to "ML" and "NLP" for data utilization and pattern recognition.

            8. **Interactive Computer Graphics**
            - *Sample Description:* Fundamental concepts oriented toward computer-aided design systems.
            - *Why it matches:* Can be relevant for "Computer Vision" skills through visual data manipulation.

            9. **Performance Modeling in Computing**
            - *Sample Description:* Introduction to probability models and techniques useful in computer science.
            - *Why it matches:* Supports "Machine Learning" by introducing necessary statistical models.

            10. **Data Visualization**
                - *Sample Description:* Introduction to computer graphics for designing and developing visualization techniques.
                - *Why it matches:* Useful for "Computer Vision" and interpreting "AI" model outputs.


            
        Please be very specific in your output and only return the titles of the courses that match the skill and small sample of the course description and why it matches the skill.

        """
    )


    # Run the matcher
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = Runner.run_sync(matcher, input=f"Skill: {skill}\nCourses: {courses}")
        return result.final_output
    finally:
        loop.close()
    

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
        title = course["course_name"]
        description = course["description"]
        formatted_courses += f"{title}\n{description}\n\n"
        
    return formatted_courses



  
