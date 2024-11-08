import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up ChromeDriver
chrome_driver_path = r'C:\Users\ryuk7\Downloads\Software\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL of the Myntra page
url = "https://www.myntra.com/men-tshirts"
driver.get(url)

# Scroll loop to load all items
scroll_pause_time = 2  # Adjust if needed
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page content
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get the fully rendered page source
html = driver.page_source
driver.quit()

# Path to save images
save_path = r"C:\Users\ryuk7\Projects\ImageClassificationClothes\data\TShirts"
os.makedirs(save_path, exist_ok=True)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all <li> elements with the class "product-base" containing product details
product_elements = soup.find_all("li", class_="product-base")
print(f"Found {len(product_elements)} product elements.")  # Debugging info

# Loop through each product element to extract and download images
for idx, product in enumerate(product_elements):
    try:
        # Find the <img> tag and use its src attribute
        img_tag = product.find("img")
        if img_tag and img_tag.get("src"):
            img_url = img_tag["src"]

            # Download the image
            img_data = requests.get(img_url).content
            with open(os.path.join(save_path, f"product_{idx + 1}.jpg"), "wb") as img_file:
                img_file.write(img_data)

            print(f"Downloaded image {idx + 1} from URL: {img_url}")

    except Exception as e:
        print(f"Could not download image {idx + 1}: {e}")
