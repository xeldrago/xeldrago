from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get("URL")  # Replace with the actual URL of the login page

# Fill in login credentials (replace with actual login details)
username_input = driver.find_element_by_id("username")
username_input.send_keys("username")
password_input = driver.find_element_by_id("password")
password_input.send_keys("pwd)

# Submit the login form
login_button = driver.find_element_by_id("login-button")
login_button.click()

# Wait for the page to load after login (adjust the timeout if needed)
#wait = WebDriverWait(driver, 10)
#wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
wait = WebDriverWait(driver, 10)
wait.until(EC.url_contains("Sub-URL"))

# Find the video element
video_elements = driver.find_elements_by_tag_name("video")

# Iterate through the video elements and download each video
for i, video_element in enumerate(video_elements):
    # Get the source URL of the video
    video_url = video_element.get_attribute("src")

    # Download the video
    response = requests.get(video_url)
    with open(f"video_{i}.mp4", "wb") as file:
        file.write(response.content)

# Close the browser
driver.quit()

