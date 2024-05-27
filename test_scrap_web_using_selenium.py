import os
import re
import logging
import json
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

products = []
final_products = []

def scrap_web():
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Open the Google homepage
    url = "https://www.boots.com/wellness/sleep/sleep-supplements"
    wait = WebDriverWait(driver, 10)
    data = driver.get(url)
    wait.until(EC.url_to_be(url))

    product_list_elem = driver.find_elements(By.CLASS_NAME, "oct-teaser__contents-panel--main-content")

    for product in product_list_elem:
        title = product.find_element(By.CSS_SELECTOR,'h3.oct-teaser__title').text.strip()
        price_with_unit = product.find_element(By.CSS_SELECTOR,'p.oct-teaser__productPrice').text.strip()
        price = float(re.sub(r'[^\x00-\x7F]', '', price_with_unit)) # Remove non-ASCII characters to extract the numeric price
        price_unit = re.findall(r'[^\x00-\x7F]',price_with_unit)[0] # Extract the price unit (currency symbol)
        product_link = product.find_element(By.CSS_SELECTOR,'a.oct-link').get_attribute('href')
        try:
            rating = product.find_element(By.CSS_SELECTOR,'div.oct-reviews__optionalText').text.strip()
        except :
            logging.warning("Review data not available for product {0}., defaulting to 0".format(str(title)))
            rating = float(0)
        
        products.append({
                        'Title': title,
                        'Price': price,
                        'Price_Unit': price_unit,
                        'Rating': rating,
                        "product_link": product_link
                    })


    for product in products:
        driver.get(product['product_link'])
        wait.until(EC.url_to_be(product_link))
        page_size = len(driver.page_source.encode('utf-8'))//1024
        short_description = driver.find_element(By.CLASS_NAME, "product_text").text
        final_products.append({
                    'Title': product['Title'],
                    'Price': product['Price'],
                    'Price_Unit': product['Price_Unit'],
                    'Rating': product['Rating'],
                    'Short_Desc': short_description,
                    "Page_Size" : page_size,
                })

    driver.quit()

def find_median(price_list):
    """
    Calculate the median of a list of prices.
    Parameters: price_list (list of float): list of prices sorted in ascending order.
    Returns: float: median value of the list.
    """
    if len(price_list) %2 == 0:
        mid = int(len(price_list)/2)
        median = (price_list[mid-1] + price_list[mid]) / 2 # Calculate the median as the average of the two middle elements
    else:
        mid = int(len(price_list)//2)
        median = price_list[mid] # The median is the middle element in the sorted list
    return median

def write_to_json(product_list_details,json_file_name):
    """
    Write product details and the median price to JSON file.
    Parameters: product_list_details (list of dict): List of dictionaries containing product details.
                json_file_name (str): The name of JSON file to write the data to.
    """

    current_working_directory = os.getcwd()
    output_folder_path = os.path.join(current_working_directory,"output")
    output_json_file_path = os.path.join(output_folder_path,json_file_name)

    logging.info("Writing the data to Json {0}.".format(output_json_file_path))

    price_list = sorted([x['Price'] for x in product_list_details])
    median = find_median(price_list) # Calculate the median price from the sorted list

    # Prepare the data to be written to the JSON file
    json_output_data = {
        'Products' : product_list_details,
        'Median' : median
    }

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Remove the existing JSON file if it exists
    if os.path.exists(output_json_file_path):
        os.remove(output_json_file_path)

    # Open the JSON file in write mode
    with open (output_json_file_path,'w',encoding='utf-8') as json_file:
        json.dump(json_output_data,json_file,indent=4,ensure_ascii=False) # Write the data to the file

    logging.info("JSON file generated Successfully.")

if __name__ == "__main__":
    try:
        scrap_web()
        write_to_json(final_products,"test.json")
    except Exception as ex:
        logging.error(str(ex))
