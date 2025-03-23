from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser
        page = browser.new_page()
        
        # Navigate to the URL
        url = "https://www.coursicle.com/njit/?search=CS"
        page.goto(url)
        
        # Wait for the page to load and any dynamic content
        page.wait_for_load_state('networkidle')
        
        # Get the page content
        content = page.content()
        
        # Print the page content
        print(content)
        
        # Take a screenshot (optional, but helpful for debugging)
        page.screenshot(path="coursicle_screenshot.png")
        
        
        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()


