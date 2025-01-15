from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Set Firefox options without proxy
firefox_options = webdriver.FirefoxOptions()

driver = webdriver.Firefox(options=firefox_options)
query = "laptops"

# Retry mechanism
max_retries = 5
for attempt in range(max_retries):
    try:
        driver.get(f"https://www.amazon.in/s?k={query}&ref=nb_sb_noss")
        elem = driver.find_element(By.CLASS_NAME, "puis-card-container")
        print(elem.get_attribute("outerHTML"))
        # print(elem.text)
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying
else:
    print("Failed to load the page after several attempts.")

driver.close()