# Sleep Aid Scraper

This Python script scrapes data from a local HTML file containing information about sleep aid products. It extracts product details such as title, price, rating, short description, and page size, and writes the information to a JSON file.

## Features

- Scrapes product data from local HTML files
- Extracts product details such as title, price, rating, and description
- Calculates the median price of the products
- Saves the extracted data and median price to a JSON file
- Logs all activities and errors for easy debugging

## Requirements

- Python 3.5 or higher
- BeautifulSoup4
- lxml

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Bala0305/WebScraper.git
cd WebScraper
```
To run this script, you need Python installed on your system along with the required dependencies. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```
## Steps to Run and test the Program

- Navigate to the project workspace
- Unzip the "Sleep Aid Clone.zip" file to your local path
- Open scraper.py file and replace the value of "html_parent_directory" variable to your unzipped "Sleep Aid Clone" folder path.
- Open Command prompt
- Execute the Below Command to run the scraper main
```bash
python scraper.py
```
- Execute the Below Command to run the test cases
```bash
python test_scraper.py
```

## Expected outcome

Description of what the correct output should look like and how to verify it.

### JSON Files

- After running the application, you should see a JSON file generated in the output directory 
- The JSON file will be generated in the below shown structure
{
    "Products": [        
        {
            "Title": "Silentnight Serenity Erase and Rewind Gift Set - Hot Water Bottle and Eye Mask Set",
            "Price": 22.99,
            "Price_Unit": "£",
            "Rating": 0.0,
            "Short_Desc": "",
            "Page_Size": 0
        }
    ],
    "Median": 11.75
}

### Log Files

The application also genereates log files that provide information about the application execution. These log files are typically located in a "logs" directory within the project

Here is an example of what the log file might look like:

2024-05-23 20:19:23,567:INFO    :Logging initiated to file Sleep_Aid_Scraper_2024-05-23_20936.log.
2024-05-23 20:19:23,567:INFO    :Web scrap Process started to extract data from Sleep Aid Web.
2024-05-23 20:19:23,567:INFO    :Started Scraping Data from D:/Assesment/Sleep Aid Clone/Sleep Aid.html.
2024-05-23 20:19:23,964:INFO    :Completed scraping data from web.
2024-05-23 20:19:23,965:INFO    :Started Extracting Product details from Soup.
2024-05-23 20:19:24,003:WARNING :Review data not available for product Boots Sleepeaze Tablets 50 mg - 20s., defaulting to 0
2024-05-23 20:19:24,003:INFO    :Started extracting short description and page size for Product.
2024-05-23 20:19:24,004:INFO    :Started Scraping Data from ./products/Boots Sleepeaze Tablets 50 mg - 20 Tablets - Boots.html.
2024-05-23 20:19:24,302:INFO    :Completed scraping data from web.
