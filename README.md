# University CS Catalog Finder

A tool that helps match university computer science courses to specific career paths by scraping course catalogs and analyzing course descriptions.

## Components

- `scrapper.py`: Scrapes course information from university catalog URLs
- `match_courses.py`: Matches courses to career-specific skills using AI
- `main.py`: Orchestrates the scraping and matching process, exports results to CSV

## Features

- Scrapes computer science course catalogs from university websites
- Matches courses to different tech career paths (AI, Frontend, Backend, etc.)
- Exports results to CSV for easy analysis
- Uses AI to intelligently match course descriptions to career skills

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
```

2. Import and use the main function in your code:
```python
from main import main

# Call the main function with required parameters
target_url = "https://cea.howard.edu/cs-course-descriptions"
career = "Frontend Engineer"

output = main(target_url, career)
```

Required Parameters:
- `target_url`: URL of the university's CS course catalog (string)
- `career`: One of the following career paths (string):
  - "AI Engineer"
  - "Frontend Engineer"
  - "Backend Engineer"
  - "Data Scientist"
  - "Cyber Security Engineer"
  - "Game Developer"

The function will:
- Scrape the specified university catalog
- Match courses to your chosen career path
- Export results to a CSV file named "courses_courses.csv"
- Return a formatted string containing the matched courses

## Example Careers
- AI Engineer
- Frontend Engineer
- Backend Engineer
- Data Scientist
- Cyber Security Engineer
- Game Developer

## Author

Created by Pablo Leyva - AI Engineer  
Connect with me on [LinkedIn](https://www.linkedin.com/in/pablo-leyva/)

## Notes

- Results depend on course catalog structure and availability
- Some universities may require authentication
- API key required for course matching functionality