from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the WebDriver (use Chrome or other browser driver)
driver_path = "/mnt/c/Users/aakas/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Update with the correct path
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run in headless mode if you don't want the browser to appear

driver = webdriver.Chrome()

# Open the target website
url = "https://www.toyota.com/4runner/features/mpg_other_price/8642/8648/8634"
driver.get(url)

# Allow time for elements to load
time.sleep(5)

# Locate and click the button to reveal hidden content (adjust selector accordingly)
try:
    buttons = driver.find_elements(By.CLASS_NAME, "show-more-button-class")  # Replace with actual class name
    for button in buttons:
        driver.execute_script("arguments[0].click();", button)  # Click all buttons

    time.sleep(3)  # Wait for content to load

    # Extract updated HTML after interactions
    page_source = driver.page_source

    # You can parse the page with BeautifulSoup if needed
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Example: Extract price or MPG data
    mpg_info = soup.find_all("div", class_="mpg-class")  # Replace with actual class name
    for mpg in mpg_info:
        print(mpg.text.strip())

except Exception as e:
    print("Error:", e)

# Close the browser
driver.quit()
