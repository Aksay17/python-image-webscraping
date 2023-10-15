import io
from pathlib import Path
import hashlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
import re

# Function to fetch the content of a specific product's webpage using Selenium.
def get_content_from_product_url(product_id):
    url = f"https://www.ecommerce.com/products/-i{product_id}.html"  # Construct the URL with the product ID.
    driver = webdriver.Chrome()  # You may need to specify the executable path if Chrome is not in the system's PATH.
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content

# Function to parse image URLs from the specified HTML element.
def parse_image_urls(content, element_class):
    soup = BeautifulSoup(content, 'html.parser')
    results = []
    for div in soup.find_all('div', class_=element_class):
        for img in div.find_all('img'):
            src = img.get('src')
            if src:
                results.append(src)
    return results

# Function to save image URLs with their respective product IDs to an Excel file.
def save_urls_to_excel(product_ids, image_urls):
    df = pd.DataFrame({"Product ID": product_ids, "Image URL": image_urls})
    df.to_excel("main_fashion_file2.xlsx", index=False)  

# Function to download and save images to a specified directory.
def get_and_save_image_to_file(image_url, output_dir):
    response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
    image_content = response.content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
    file_path = output_dir / filename
    image.save(file_path, "PNG", quality=80)

# Main function
# C:\scra
# Main function
def main(product_ids):
    product_ids_with_urls = []  # Create a list to store product IDs with corresponding image URLs.
    image_urls = []
   
    for product_id in product_ids:
        content = get_content_from_product_url(product_id)
        product_image_urls = parse_image_urls(
            content=content, element_class="html-content detail",  # Replace with the actual class name.
        )
        image_urls.extend(product_image_urls)
       
        # Ensure that the product_ids and image_urls lists have the same length.
        num_image_urls = len(product_image_urls)
        product_ids_with_urls.extend([product_id] * num_image_urls)

    save_urls_to_excel(product_ids_with_urls, image_urls)

    for image_url in image_urls:
        get_and_save_image_to_file(
            image_url, output_dir=Path("C:\scra"),  # Replace with the desired output directory.
        )

if __name__ == "__main__":
    product_ids = [""]  # Add the list of product IDs you want to search for.
    main(product_ids)
