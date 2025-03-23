import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapegraphai.graphs import SmartScraperGraph
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import json
import os
# Find all clickable elements
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def wait_for_element(driver, by, value, timeout=10, description="element", wait_type="clickable"):
    try:
        wait = WebDriverWait(driver, timeout)
        if wait_type == "clickable":
            element = wait.until(
                EC.element_to_be_clickable((by, value))
            )
        elif wait_type == "visible":
            element = wait.until(
                EC.visibility_of_element_located((by, value))
            )
        else:
            element = wait.until(
                EC.presence_of_element_located((by, value))
            )
        return element
    except TimeoutException:
        print(f"Timeout waiting for {description} to {wait_type}. Retrying...")
        return None

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start with max window
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hide automation
chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize the service with the path to ChromeDriver
service = Service('/usr/bin/chromedriver')

# Create the Remote WebDriver with options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set a script to disable navigator.webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Navigate to the page
    driver.get('https://www.coursicle.com/njit/?search=CS')
    
    # Wait for initial page load with longer timeout
    print("Waiting for page to load...")
    time.sleep(10)  # Give more time for initial load
    
    # Try different selectors for the results container
    selectors_to_try = [
        (By.ID, "classSearchResultsContainer"),
        (By.CLASS_NAME, "classSearchItem"),
        (By.CLASS_NAME, "classSearchResults")
    ]
    
    results_container = None
    for by, selector in selectors_to_try:
        print(f"Trying to find results with selector: {selector}")
        results_container = wait_for_element(driver, by, selector, timeout=15, description=f"results container ({selector})")
        if results_container:
            print(f"Found results container using {selector}")
            break
    
    if not results_container:
        raise Exception("Could not find results container with any selector")
    
    # Now get all class items after everything is loaded
    class_items = driver.find_elements(By.CLASS_NAME, "classSearchItem")
    
    if not class_items:
        print("No class items found. Taking screenshot for debugging...")
        driver.save_screenshot("debug_screenshot.png")
        raise Exception("No class items found on the page")
    
    print(f"Total class sections found: {len(class_items)}")
    
    # Keep track of unique courses
    seen_courses = set()
    
    # Extract information from each class item
    for item in class_items:
        try:
            # Get the data-klass attribute which contains class details
            class_data = item.get_attribute('data-klass')
            if class_data:
                class_info = json.loads(class_data)
                
                # Extract the base course number (before the hyphen)
                course_number = class_info.get('class', '').split('-')[0]
                course_title = class_info.get('title', '')
                
                # Create a unique identifier for the course
                course_identifier = f"{course_number}:{course_title}"
                
                # Skip if we've already seen this course
                if course_identifier in seen_courses:
                    continue
                    
                seen_courses.add(course_identifier)
                
                print(f"\nProcessing course: {course_number}")
                
                # Click the item to expand it
                try:
                    # First ensure the element is in view
                    driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    time.sleep(0.5)  # Wait for scroll to complete
                    
                    # Try to click using different methods
                    try:
                        item.click()
                    except ElementClickInterceptedException:
                        # If normal click fails, try JavaScript click
                        driver.execute_script("arguments[0].click();", item)
                    
                    # Wait for description to be visible with longer timeout
                    description_element = wait_for_element(
                        driver,
                        By.CLASS_NAME,
                        "subItemContent",
                        timeout=10,
                        description="course description",
                        wait_type="visible"
                    )
                    
                    if description_element:
                        # Wait a moment for text to load
                        time.sleep(0.5)
                        description = description_element.text
                        if description:
                            print(f"Class: {course_number}")
                            print(f"Title: {course_title}")
                            print(f"Description: {description}")
                            print("-------------------")
                        else:
                            print(f"No description text found for {course_number}")
                    
                    # Wait a bit before moving to next item
                    time.sleep(1)
                except Exception as click_error:
                    print(f"Error clicking or getting description for {course_number}: {click_error}")
                    continue
                
        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    print(f"\nTotal unique courses found: {len(seen_courses)}")

except Exception as e:
    print(f"An error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    
finally:
    print("Closing browser...")
    driver.quit()