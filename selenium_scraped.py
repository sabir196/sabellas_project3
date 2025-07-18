from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Launch browser ---
print("🚀 Launching Chrome browser...")
driver = webdriver.Chrome()
driver.get("https://pickupportal.com/login/")

# --- Log in ---
time.sleep(2)
driver.find_element(By.ID, "user_login").send_keys("ryanjames530@gmail.com")
driver.find_element(By.ID, "user_pass").send_keys("sapte5-vexdyn-rodgYv")
driver.find_element(By.ID, "user_pass").send_keys(Keys.RETURN)

# --- Wait for login redirect ---
time.sleep(5)

# --- Go to player lookup page ---
driver.get("https://pickupportal.com/lookup/?type=player")
print("📄 Opened player lookup page")
time.sleep(2)

# --- Accept cookies if visible ---
try:
    accept_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
    )
    accept_btn.click()
    print("🍪 Accepted cookies banner")
except:
    print("🔍 No cookie banner detected")

# --- Select "Baseball" from dropdown ---
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "player_sport_type"))
    )
    dropdown = Select(driver.find_element(By.ID, "player_sport_type"))
    dropdown.select_by_visible_text("Baseball")
    print("✅ Selected sport:", dropdown.first_selected_option.text)
except Exception as e:
    print("❌ Failed to select dropdown:", e)

# --- Scroll & click Search button with JS ---
try:
    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", search_btn)
    print("🖱️ Clicked Search button using JavaScript")
except Exception as e:
    print("❌ Search button click failed:", e)

# --- Wait for player profiles to load ---
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "player-box-h4"))
    )
    print("✅ Player profiles loaded.")
except Exception as e:
    print("❌ Player profiles not found:", e)

# --- Save the page HTML ---
output_path = "/Users/sababa/Downloads/players_selenium.html"
html = driver.page_source
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
print(f"✅ Done. Saved HTML to: {output_path}")
