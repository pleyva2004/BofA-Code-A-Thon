from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Add options to make selenium less detectable
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Create driver with options
driver = webdriver.Chrome(options=options)

# Update the window size to a common resolution
driver.set_window_size(1920, 1080)

# Add a random delay between 2 and 5 seconds
time.sleep(random.uniform(2, 5))

driver.get("https://www.coursicle.com/njit/?search=CS")

# Wait for page to load with random delay
time.sleep(random.uniform(8, 12))








