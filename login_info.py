from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import getpass

# Prompt for credentials
email = input("Enter your Pickup Portal email: ")
password = getpass.getpass("Enter your password (input hidden): ")

# Set up Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Navigate to login page
    driver.get("https://pickupportal.com/login")

    print("🟡 Waiting for login page to load...")
    time.sleep(3)  # wait for form to load

    # Enter email and password
    driver.find_element(By.ID, "user_login").send_keys(email)
    driver.find_element(By.ID, "user_pass").send_keys(password)

    # Submit form
    driver.find_element(By.NAME, "wp-submit").click()
    print("✅ Login submitted!")

    # Wait to verify login worked
    time.sleep(5)

    # You can now keep the session alive or return the driver to another script
    input("🟢 Logged in. Press Enter to close browser...")

finally:
    driver.quit()
