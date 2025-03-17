from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from agents import set_default_openai_key
from agents import set_tracing_export_api_key
from pydantic import BaseModel
import os
import requests
from typing import Optional
from urllib.parse import urlparse
import re

set_default_openai_key(os.getenv("OPENAI_API_KEY"))
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))

class URLVerificationResult(BaseModel):
    url: str
    is_valid: bool
    domain_verified: bool
    is_accessible: bool
    contains_cs_courses: bool
    error_message: Optional[str] = None

class URLNormalizer:
    @staticmethod
    def normalize_url(url: str, university_name: str) -> str:
        """Normalize URLs based on university-specific patterns"""
        url_lower = url.lower()
        university_lower = university_name.lower()

        # Common URL transformations for specific universities
        university_patterns = {
            'stanford': {
                'old_patterns': [
                    'exploredegrees.stanford.edu/schoolofengineering/computerscience',
                    'exploredegrees.stanford.edu/computerscience'
                ],
                'new_pattern': 'bulletin.stanford.edu/departments/COMPUTSCI/courses'
            },
            'berkeley': {
                'old_patterns': ['guide.berkeley.edu/courses'],
                'new_pattern': 'www2.eecs.berkeley.edu/Courses/CS'
            },
            'mit': {
                'old_patterns': ['catalog.mit.edu'],
                'new_pattern': 'student.mit.edu/catalog/m6a.html'
            }
        }

        # Check for university-specific transformations
        for uni, patterns in university_patterns.items():
            if uni in university_lower:
                for old_pattern in patterns['old_patterns']:
                    if old_pattern in url_lower:
                        return f"https://{patterns['new_pattern']}"

        return url

def verify_url(url: str, university_name: str = "") -> URLVerificationResult:
    try:
        # Parse URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return URLVerificationResult(
                url=url,
                is_valid=False,
                domain_verified=False,
                is_accessible=False,
                contains_cs_courses=False,
                error_message="Invalid URL format"
            )

        # Normalize URL based on university patterns
        normalized_url = URLNormalizer.normalize_url(url, university_name)
        
        # If URL was normalized, update the parsed URL
        if normalized_url != url:
            url = normalized_url
            parsed = urlparse(url)

        # Check if domain is .edu or known university domain
        domain_verified = parsed.netloc.endswith('.edu') or any(
            known_domain in parsed.netloc 
            for known_domain in ['university', 'college', 'institute', 'uni.']
        )

        # Check if URL is accessible
        response = requests.get(url, timeout=10, allow_redirects=True)
        is_accessible = response.status_code == 200

        # Enhanced content checking for CS course indicators
        content = response.text.lower()
        
        # University-specific content patterns
        university_content_patterns = {
            'stanford': {
                'course_patterns': [
                    r'cs\s*\d{2,3}[a-z]?',  # CS 106A, CS 229, etc.
                    r'computer science.*?units',
                    r'bulletin.*?courses'
                ]
            },
            'berkeley': {
                'course_patterns': [
                    r'compsci\s*\d{2,3}[a-z]?',
                    r'cs\s*\d{2,3}[a-z]?'
                ]
            },
            'mit': {
                'course_patterns': [
                    r'6\.\d{3,4}',  # MIT's course numbering
                    r'course\s*6'
                ]
            }
        }

        # Add university-specific patterns if available
        additional_patterns = []
        for uni, patterns in university_content_patterns.items():
            if uni in university_name.lower():
                additional_patterns.extend(patterns['course_patterns'])

        # Common course section anchors with priority order
        course_section_patterns = [
            '#coursestext',
            '#courses',
            '#course-list',
            '#course-descriptions',
            '#programrequirementstext',
            '#curriculum'
        ]
        
        # If URL doesn't end with a course section pattern, try to find one
        if not any(url.endswith(pattern) for pattern in course_section_patterns):
            # Only append anchor if the base URL doesn't already point to a course listing
            if not any(re.search(pattern, content) for pattern in additional_patterns):
                base_url = url.split('#')[0]
                for pattern in course_section_patterns:
                    if pattern in content:
                        url = f"{base_url}{pattern}"
                        break

        # Enhanced CS course indicators with more specific patterns
        cs_indicators = [
            'computer science',
            'course description',
            'undergraduate courses',
            'cs courses',
            'course catalog',
            'degree requirements',
            'course number',
            'credits',
            'prerequisites',
            'cs \d{3}',
            'computer science courses'
        ]
        
        # Combine common patterns with university-specific ones
        course_listing_indicators = [
            'cs \d{3}',
            'comp \d{3}',
            'computer science \d{3}',
            'course number.*?description',
            'credits.*?prerequisites'
        ] + additional_patterns
        
        contains_cs_courses = (
            any(indicator in content for indicator in cs_indicators) or
            any(re.search(pattern, content, re.IGNORECASE) for pattern in course_listing_indicators)
        )

        return URLVerificationResult(
            url=url,
            is_valid=True,
            domain_verified=domain_verified,
            is_accessible=is_accessible,
            contains_cs_courses=contains_cs_courses
        )

    except Exception as e:
        return URLVerificationResult(
            url=url,
            is_valid=False,
            domain_verified=False,
            is_accessible=False,
            contains_cs_courses=False,
            error_message=str(e)
        )

class UniversityCatalogOutput(BaseModel):
    university_name: str
    catalog_url: str
    verification_status: URLVerificationResult

verification_instructions = """
You are a URL verification specialist. Your task is to:
1. Verify that the provided URL is from an official university domain
2. Check if the URL is accessible
3. Confirm that the page contains computer science course information
4. Return detailed verification results
"""

verification_agent = Agent(
    name="URL Verification Agent",
    instructions=verification_instructions,
    output_type=URLVerificationResult
)

async def url_verification_guardrail(ctx, agent, input_data):
    if isinstance(input_data, str) and input_data.startswith('http'):
        result = verify_url(input_data)
        return GuardrailFunctionOutput(
            output_info=result,
            tripwire_triggered=not (result.is_valid and result.domain_verified and result.is_accessible)
        )
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

web_scraping_instructions = """
Task: Given the name of a university or college, find the official undergraduate catalog page that lists all available Computer Science courses, including course descriptions and degree requirements.

Instructions:

1. Search for the official undergraduate catalog or bulletin of the given institution.
2. Locate the Computer Science (CS) program within the undergraduate catalog.
3. Extract the direct URL that provides a comprehensive list of all undergraduate CS courses, including descriptions.
4. If multiple links exist, prioritize the one that includes detailed course descriptions and requirements.
5. Ensure that the URL is from an official university domain (e.g., .edu or an official subdomain).
6. Return "No Computer Science catalog found" if no valid URL is found.

URL Patterns to prioritize (in order):
1. /catalog/*/computer-science/#coursestext
2. /catalog/*/computer-science/#courses
3. /catalog/*/computer-science/#programrequirementstext
4. /catalog/*/cs/#coursestext
5. /courses/computer-science/
6. /cs/courses/
7. /computerscience/undergraduate/

Important URL refinements:
- For catalog URLs, always check if there's a #coursestext or #courses anchor available
- Verify that the page contains actual course listings with course numbers and descriptions
- Prefer URLs that directly link to the course descriptions section
- If a base catalog URL is found, try to append the appropriate anchor (#coursestext, #courses, etc.)

Response format:
{
    "university_name": "University Name",
    "catalog_url": "URL or 'No Computer Science catalog found'",
    "verification_status": URLVerificationResult
}
"""

agent = Agent(
    name="Web Scraping Agent",
    instructions=web_scraping_instructions,
    output_type=UniversityCatalogOutput,
    input_guardrails=[
        InputGuardrail(guardrail_function=url_verification_guardrail),
    ]
)

async def get_university_catalog(university_name: str) -> UniversityCatalogOutput:
    """
    Get the computer science course catalog URL for a given university.
    
    Args:
        university_name: Name of the university
        
    Returns:
        UniversityCatalogOutput object containing the URL and verification status
    """
    result = await Runner.run(agent, university_name)
    
    # If we got a URL, verify and potentially normalize it
    if hasattr(result, 'final_output') and result.final_output.catalog_url != "No Computer Science catalog found":
        verification_result = verify_url(result.final_output.catalog_url, university_name)
        result.final_output.verification_status = verification_result
        result.final_output.catalog_url = verification_result.url
    
    return result.final_output


if __name__ == "__main__":
    # Example usage
    university_name = input("Enter university name: ")
    result = get_university_catalog(university_name)
    print("\nResults:")
    print(f"University: {result.university_name}")
    print(f"Catalog URL: {result.catalog_url}")

    print("\nVerification Status:")
    print(f"Domain Verified: {result.verification_status.domain_verified}")
    print(f"Page Accessible: {result.verification_status.is_accessible}")
    print(f"Contains CS Courses: {result.verification_status.contains_cs_courses}")
    if result.verification_status.error_message:
        print(f"Error: {result.verification_status.error_message}")

    # Run the async main function


