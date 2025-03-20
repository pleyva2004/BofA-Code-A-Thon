# University CS Catalog Finder

This program helps users find computer science course catalogs for universities by searching the web for relevant URLs.

## Features

- Simple command-line interface
- Searches for official university course catalogs
- Filters results to find computer science-specific catalog pages
- Easy to use interactive prompt

## Installation

1. Clone this repository or download the source files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
```bash
python university_catalog_finder.py
```

2. Enter the name of the university when prompted
3. The program will search for and display the URL of the computer science course catalog
4. Type 'quit' to exit the program

## Example

```
Welcome to the University CS Catalog Finder!
This program helps you find computer science course catalogs for universities.

Enter university name (or 'quit' to exit): University of Illinois Chicago

Searching for University of Illinois Chicago's computer science course catalog...

Found course catalog URL: https://catalog.uic.edu/ucat/course-descriptions/cs/
```

## Notes

- The program uses web scraping to find catalog URLs, so results may vary depending on university website structures
- Some universities may require authentication to access their course catalogs
- The program attempts to find the most relevant URL but may occasionally return incorrect results

## Requirements

- Python 3.6 or higher
- requests library
- beautifulsoup4 library