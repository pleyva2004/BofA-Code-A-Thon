import requests
from bs4 import BeautifulSoup
import re
import json
import time
import argparse
from urllib.parse import urljoin

class UniversityScraper:
    def __init__(self, university_name):
        self.university_name = university_name
        self.base_urls = self._get_base_urls()
        self.courses = []
        
    def _get_base_urls(self):
        """Map university names to their course catalog URLs and scraping patterns."""
        university_map = {
            "stanford university": {
                "catalog_url": "https://explorecourses.stanford.edu/search?q=CS&view=catalog&filter-coursestatus-Active=on",
                "course_pattern": "div.courseInfo",
                "title_pattern": "span.courseTitle, span.courseNumber",
                "description_pattern": "div.courseDescription",
                "dept_keywords": ["CS", "Computer Science", "Data Science", "Artificial Intelligence"]
            },
            "mit": {
                "catalog_url": "http://catalog.mit.edu/subjects/#cstext",
                "course_pattern": "div.courseblock",
                "title_pattern": "p.courseblocktitle",
                "description_pattern": "p.courseblockdesc",
                "dept_keywords": ["6.", "Computer Science", "Electrical Engineering", "EECS"]
            },
            "harvard university": {
                "catalog_url": "https://courses.my.harvard.edu/psp/courses/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH",
                "course_pattern": "div.class-info",
                "title_pattern": "div.class-title",
                "description_pattern": "div.class-description",
                "dept_keywords": ["CS", "Computer Science", "Data Science"]
            },
            "university of california berkeley": {
                "catalog_url": "https://guide.berkeley.edu/courses/compsci/",
                "course_pattern": "div.courseblock",
                "title_pattern": "p.courseblocktitle",
                "description_pattern": "p.courseblockdesc",
                "dept_keywords": ["COMPSCI", "Computer Science", "Data Science", "INFO"]
            },
            "carnegie mellon university": {
                "catalog_url": "https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search",
                "course_pattern": "tr.course-row",
                "title_pattern": "td.title",
                "description_pattern": "td.description",
                "dept_keywords": ["15-", "Computer Science", "Machine Learning", "Artificial Intelligence"]
            }
        }
        
        # Default generic approach if university not in map
        default_map = {
            "catalog_url": f"https://www.google.com/search?q={self.university_name.replace(' ', '+')}+computer+science+undergraduate+courses",
            "course_pattern": None,  # Will need to be determined dynamically
            "title_pattern": None,
            "description_pattern": None,
            "dept_keywords": ["CS", "Computer Science", "Data Science", "Artificial Intelligence", 
                             "Machine Learning", "Computational", "Computing"]
        }
        
        # Find the closest match or return default
        for univ, data in university_map.items():
            if univ.lower() in self.university_name.lower() or self.university_name.lower() in univ.lower():
                return data
                
        return default_map
    
    def scrape_courses(self):
        """Main method to scrape courses based on university patterns."""
        print(f"Scraping CS courses for {self.university_name}...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(self.base_urls["catalog_url"], headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Failed to access catalog. Status code: {response.status_code}")
                return False
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # If we have specific patterns, use them
            if self.base_urls["course_pattern"]:
                self._extract_with_patterns(soup)
            else:
                # Otherwise try to find course information dynamically
                self._extract_dynamically(soup)
                
            print(f"Found {len(self.courses)} CS-related courses.")
            return True
            
        except Exception as e:
            print(f"Error scraping {self.university_name}: {str(e)}")
            return False
    
    def _extract_with_patterns(self, soup):
        """Extract courses using predefined patterns."""
        course_elements = soup.select(self.base_urls["course_pattern"])
        
        for course in course_elements:
            # Extract title
            if self.base_urls["title_pattern"]:
                title_element = course.select_one(self.base_urls["title_pattern"])
                title = title_element.text.strip() if title_element else "No title found"
            else:
                title = "Title extraction pattern not specified"
                
            # Extract description
            if self.base_urls["description_pattern"]:
                desc_element = course.select_one(self.base_urls["description_pattern"])
                description = desc_element.text.strip() if desc_element else "No description found"
            else:
                description = "Description extraction pattern not specified"
                
            # Check if the course is CS-related
            is_cs_related = False
            for keyword in self.base_urls["dept_keywords"]:
                if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                    is_cs_related = True
                    break
                    
            if is_cs_related:
                self.courses.append({
                    "title": title,
                    "description": description
                })
    
    def _extract_dynamically(self, soup):
        """
        Attempt to dynamically find and extract course information based on common patterns.
        This is a fallback when specific patterns aren't known.
        """
        # Look for links to the course catalog
        catalog_links = []
        for a in soup.find_all('a'):
            text = a.text.lower()
            href = a.get('href', '')
            
            # Check if the link might lead to course catalog
            catalog_keywords = ['course', 'catalog', 'curriculum', 'program', 'computer science']
            if any(keyword in text for keyword in catalog_keywords) or any(keyword in href for keyword in catalog_keywords):
                url = urljoin(self.base_urls["catalog_url"], href)
                catalog_links.append(url)
        
        # If we found potential catalog links, follow them
        if catalog_links:
            for link in catalog_links[:3]:  # Limit to first 3 to avoid too many requests
                try:
                    print(f"Following catalog link: {link}")
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(link, headers=headers, timeout=10)
                    if response.status_code == 200:
                        catalog_soup = BeautifulSoup(response.text, 'html.parser')
                        self._identify_course_patterns(catalog_soup)
                except Exception as e:
                    print(f"Error following catalog link {link}: {str(e)}")
        else:
            # Try to find course information on the current page
            self._identify_course_patterns(soup)
    
    def _identify_course_patterns(self, soup):
        """Try to identify common course listing patterns."""
        # Common patterns for course listings
        patterns = [
            {'container': 'div.course', 'title': 'h3', 'desc': 'p'},
            {'container': 'div.courseblock', 'title': '.courseblocktitle', 'desc': '.courseblockdesc'},
            {'container': 'tr.course-row', 'title': 'td.title', 'desc': 'td.description'},
            {'container': 'div.course-info', 'title': 'h4', 'desc': 'div.description'},
            {'container': 'li.course', 'title': 'strong', 'desc': 'p'},
        ]
        
        for pattern in patterns:
            containers = soup.select(pattern['container'])
            if containers:
                print(f"Found {len(containers)} possible course containers with pattern {pattern['container']}")
                for container in containers:
                    title_elem = container.select_one(pattern['title'])
                    desc_elem = container.select_one(pattern['desc'])
                    
                    title = title_elem.text.strip() if title_elem else "No title found"
                    description = desc_elem.text.strip() if desc_elem else "No description found"
                    
                    # Check if CS-related
                    is_cs_related = False
                    for keyword in self.base_urls["dept_keywords"]:
                        if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                            is_cs_related = True
                            break
                            
                    if is_cs_related:
                        self.courses.append({
                            "title": title,
                            "description": description
                        })
        
        # If still no courses found, try even more generic approach
        if not self.courses:
            # Look for text that contains CS course codes (e.g., CS 101, COMP 110)
            course_code_pattern = re.compile(r'(CS|COMP|COMPSCI|CSE|CIS)\s*\d{3}')
            for tag in soup.find_all(['h3', 'h4', 'strong', 'p', 'div']):
                if course_code_pattern.search(tag.text):
                    # If course code found, get next paragraph as description
                    title = tag.text.strip()
                    desc_tag = tag.find_next('p')
                    description = desc_tag.text.strip() if desc_tag else "No description found"
                    
                    self.courses.append({
                        "title": title,
                        "description": description
                    })
    
    def save_to_json(self, filename=None):
        """Save the scraped courses to a JSON file."""
        if not filename:
            # Create a filename based on university name
            safe_name = re.sub(r'[^\w\s]', '', self.university_name).lower().replace(' ', '_')
            filename = f"{safe_name}_cs_courses.json"
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "university": self.university_name,
                "courses": self.courses,
                "total_courses": len(self.courses)
            }, f, indent=4)
            
        print(f"Saved {len(self.courses)} courses to {filename}")
        return filename

def main():
    parser = argparse.ArgumentParser(description='Scrape computer science courses from a university.')
    parser.add_argument('university', type=str, help='Name of the university')
    parser.add_argument('--output', type=str, help='Output JSON filename', default=None)
    
    args = parser.parse_args()
    
    scraper = UniversityScraper(args.university)
    success = scraper.scrape_courses()
    
    if success and scraper.courses:
        filename = scraper.save_to_json(args.output)
        print(f"Successfully scraped courses and saved to {filename}")
    else:
        print(f"Failed to scrape courses for {args.university}")

if __name__ == "__main__":
    main()