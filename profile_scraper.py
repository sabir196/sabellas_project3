from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time
from getpass import getpass

# Setup Selenium options
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Get user credentials securely
email = input("Enter your Pickup Portal email: ")
password = getpass("Enter your password (input hidden): ")

print("🔹 Waiting for login page to load...")
driver.get("https://pickupportal.com/login/")

# Login
driver.find_element(By.ID, "user_login").send_keys(email)
driver.find_element(By.ID, "user_pass").send_keys(password)
driver.find_element(By.ID, "wp-submit").click()
time.sleep(5)
print("✅ Login submitted!")

# Connect to SQLite database
conn = sqlite3.connect('/Users/sababa/Downloads/players.db')
cursor = conn.cursor()

# Load player profile links where email is still null (not scraped yet)
cursor.execute("""
    SELECT id, profile_link 
    FROM players 
    WHERE profile_link IS NOT NULL 
      AND email IS NULL 
    LIMIT 10
""")
players = cursor.fetchall()

MAX_ERRORS = 10
error_count = 0

for player_id, profile_link in players:
    try:
        driver.get(profile_link)
        time.sleep(3)

        # Click Contact Parent if it exists
        try:
            contact_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Contact Parent')]")
            contact_button.click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]"))
            )
        except Exception as e:
            print(f"⚠️ Could not click or load Contact Parent info on: {profile_link}")

        # Scrape fields
        def try_xpath(xpath):
            try:
                return driver.find_element(By.XPATH, xpath).text.strip()
            except:
                return None

        name = try_xpath("//span[@class='status-name' and text()='NAME:']/following-sibling::span")
        date_of_birth = try_xpath("//span[@class='status-name' and text()='BIRTHDAY:']/following-sibling::span")
        email = try_xpath("//a[starts-with(@href, 'mailto:')]")
        phone = try_xpath("//a[starts-with(@href, 'tel:')]")
        primary_position = try_xpath("//span[@class='status-name' and text()='PRIMARY POSITION:']/following-sibling::span")
        secondary_position = try_xpath("//span[@class='status-name' and text()='SECONDARY POSITION:']/following-sibling::span")
        team = try_xpath("//span[@class='status-name' and text()='TEAM:']/following-sibling::span")
        available_dates = try_xpath("//span[@class='status-name' and text()='AVAILABLE DATES:']/following-sibling::span")

        # Update database
        cursor.execute("""
            UPDATE players 
            SET name = ?, date_of_birth = ?, email = ?, phone = ?, 
                primary_position = ?, secondary_position = ?, 
                team = ?, available_dates = ?
            WHERE id = ?
        """, (name, date_of_birth, email, phone, primary_position, secondary_position, team, available_dates, player_id))
        conn.commit()

        print(f"✅ Scraped: {profile_link}")
        error_count = 0

    except Exception as e:
        print(f"❌ Error scraping {profile_link}: {e}")
        error_count += 1
        if error_count >= MAX_ERRORS:
            print("❌ Too many consecutive errors. Stopping.")
            break

# Cleanup
driver.quit()
conn.close()
print("✅ Done scraping profiles.")
