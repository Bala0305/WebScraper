import os
import re
import sys
import json
import logging
import datetime
from bs4 import BeautifulSoup
from urllib.parse import unquote

 # Define the JSON file name where product details will be stored
json_file_name = "product_details.json"

# Define the directory and file name of the HTML file to be processed
html_parent_directory = "D:/Assesment/Sleep Aid Clone/"
html_parent_file_name = os.path.join(html_parent_directory,"Sleep Aid.html")


def scrap_data_from_web(html_file_name):
    """
    Scrape data from local HTML file and return  BeautifulSoup object.
    Parameters: html_file_name (str): The name of HTML file to parsed.
    Returns: BeautifulSoup: BeautifulSoup object containing the HTML content.
    """
    try:
        logging.info("Started Scraping Data from {0}.".format(str(html_file_name)))

        if not os.path.exists(html_file_name):
            raise Exception("File not exists : {0}.".format(html_file_name))

        with open(html_file_name,'r',encoding='utf-8') as html_file:
            html_content = html_file.read()
            soup = BeautifulSoup(html_content,'lxml')
            logging.info("Completed scraping data from web.")
            return soup
        
    except Exception as ex:
        logging.error("Failed to Scrap data from {0}.".format(str(html_file_name)))
        logging.error("Failed due to the error {0}.".format(str(ex)))
        raise Exception(str(ex))  # Raise the exception to be handled by the caller

def extract_product_info(soup):
    """
    Extract product information from BeautifulSoup object.
    Parameters: soup (BeautifulSoup): BeautifulSoup object containing HTML content.
    Returns: list of dict: list of dictionaries containing details of product.
    """
    logging.info("Started Extracting Product details from Soup.")
    products = []
    for product in soup.find_all('div', class_='oct-teaser__contents-panel--main-content'):
        title = product.find('h3',class_ = 'oct-teaser__title').text.strip()
        price_with_unit = product.find('p',class_ = 'oct-teaser__productPrice').text.strip()
        price = float(re.sub(r'[^\x00-\x7F]', '', price_with_unit)) # Remove non-ASCII characters to extract the numeric price
        price_unit = re.findall(r'[^\x00-\x7F]',price_with_unit)[0] # Extract the price unit (currency symbol)
       
        # Attempt to extract the product rating, default to 0 if not available
        try:
            rating = float(product.find('div',class_ = 'oct-reviews__optionalText').find('a')['aria-label'][:4])
        except :
            logging.warning("Review data not available for product {0}., defaulting to 0".format(str(title)))
            rating = float(0)        
        
        product_link = unquote(product.find('a',class_ = 'oct-teaser__title-link')['href']) # Extract the product link and decode it
        product_file_name = os.path.join(html_parent_directory,product_link)
        short_description , page_size = extract_short_description_and_size(product_file_name)
        
        products.append({
                    'Title': title,
                    'Price': price,
                    'Price_Unit': price_unit,
                    'Rating': rating,
                    'Short_Desc': short_description,
                    "Page_Size" : page_size,
                })
    logging.info("Completed Extracting Product details from Soup.")
    return products

def extract_short_description_and_size(product_file_name):
    """
    Extract the short description and page size for a given product.
    Parameters: product_file_name (str): file name of the product HTML file.
    Returns: tuple: tuple containing short description (str) and the size of page in KB (float).
    """
    try:
        logging.info("Started extracting short description and page size for Product.")

        # Scrape product detail from the web using the given file name
        product_detail = scrap_data_from_web(product_file_name)

        try:
            product_text = product_detail.find('div',class_ = 'product_text')
            short_description = product_text.find('p',itemprop = 'description').text
            print("available")
        except:
            short_description = ""
            logging.warning("Defaulting short_description to empty string")

        size = len(str(product_detail).encode('utf-8'))/1024 # Calculate the size of the page in kilobytes (KB)

        logging.info("Completed extracting short description and page size for Product.")
        return short_description , int(size)
    
    except Exception as ex:
        logging.warning("fallback enabled as {0}.".format(str(ex)))
        logging.warning("Defaulting Short_description to empty string and Size to 0.")
        return "" , 0  # Return default values: an empty short description and size 0 KB
    
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

def setup_logging(process_name):
    """
    Set up logging configuration for the script.
    Parameters: process_name (str): name of the process to include in the log file name.
    """
    # Get the current working directory
    current_working_directory = os.getcwd()
    log_directory = os.path.join(current_working_directory,"logs")

    # Create the log directory if it does not exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    process_id = str(os.getpid()) # Get the current process ID
    log_file_name = "{0}_{1}_{3}.log".format(process_name,str(datetime.date.today()),str(datetime.datetime.now().time()),process_id)
    log_file_path = os.path.join(log_directory,log_file_name)

    logging.basicConfig(filename=log_file_path,filemode='a',format='%(asctime)-10s:%(levelname)-8s:%(message)s',level=logging.INFO)
    
    # Set up logging to the console (standard output)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)-10s:%(levelname)-8s:%(message)s'))
    logging.getLogger().addHandler(console)

    logging.info("Logging initiated to file {0}.".format(log_file_name))

def main():
    """
    Main function to perform the web scraping process.
    It reads HTML content, extracts product information, and writes it to JSON file.
    """
    # Scrape data from the web page using the specified HTML file
    web_soup = scrap_data_from_web(html_parent_file_name)

    # Extract product information from the scraped web data
    product_list_details = extract_product_info(web_soup)

    # Write the extracted product information to a JSON file
    write_to_json(product_list_details,json_file_name)

if __name__ == "__main__":

    # Initialize logging for the script
    setup_logging("Sleep_Aid_Scraper") 

    try:
        logging.info("Web scrap Process started to extract data from Sleep Aid Web.")
        main() # Call the main function to perform the web scraping
        logging.info("Web scrap Completed Successfully.")
        sys.exit(0) #Exit the script with a status code of 0 (success)

    except Exception as ex:
        logging.error("Web scrap process Failed.")
        logging.error("Failed due to the error {0},".format(str(ex)))
        sys.exit(1) #Exit the script with a status code of 1 (error)
