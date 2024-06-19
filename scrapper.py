from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your ChromeDriver executable
chrome_driver_path = 'C:/Users/piotr/Desktop/Magisterka/chromrdriver/chromedriver-win64/chromedriver.exe'  # Update this path to the actual path

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Optional: start maximized

# Initialize the Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open a website
driver.get("https://www.hltv.org/matches/2373216/case-vs-insanity-dust2-brasil-liga-bcgame-season-3")  # Replace with the URL you want to monitor

# Handle popup (if any)
try:
    # Wait for the popup to appear
    popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialog')))
    print("Popup detected, handling...")
    
    # Example action to close the popup
    popup.find_element(By.ID, 'CybotCookiebotDialogBodyButtonAccept').click()  # Adjust with the actual close action
    
    # Wait for the popup to close (if necessary)
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'CybotCookiebotDialog')))
    
    print("Popup closed successfully.")
except Exception as e:
    print("Popup did not appear within expected time or does not exist.")

# Handle captcha or user interaction (example: "I'm not a robot")
try:
    # Example: Solve captcha or interact with user interaction elements
    captcha_input = driver.find_element(By.ID, 'captcha-input')  # Replace with actual captcha element locator
    captcha_input.send_keys("example-captcha-solution")  # Replace with actual captcha solution
    
    # Example: Click submit button after solving captcha
    submit_button = driver.find_element(By.ID, 'submit-button')  # Replace with actual submit button locator
    submit_button.click()
    
    print("Captcha solved or interaction completed.")
except Exception as e:
    print(f"Error handling captcha or interaction: {e}")

# Continue script execution (example: fetch content after interaction)
try:
    # Wait for the scoreboard element to be present
    parent_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'scoreboard')))
    
    # Locate the nested element with class 'score scoreText' using CSS selector
    nested_element_css = parent_element.find_element(By.CSS_SELECTOR, '.score.scoreText')
    # Get the text content of the nested element
    content_css = nested_element_css.text
    print(f"Content of the nested element with class name 'score scoreText' using CSS selector: {content_css}")
    
    # Locate the nested element with class 'score scoreText' using XPath
    nested_element_xpath = parent_element.find_element(By.XPATH, ".//*[contains(@class, 'score') and contains(@class, 'scoreText')]")
    # Get the text content of the nested element
    content_xpath = nested_element_xpath.text
    print(f"Content of the nested element with class name 'score scoreText' using XPath: {content_xpath}")
    
except Exception as e:
    print(f"Error locating element by class name: {e}")

# Delay before quitting (allow time for observations)
time.sleep(10)  # Adjust as necessary

# Close the browser
driver.quit()
