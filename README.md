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
pip install beautifulsoup4
pip install lxml
```
## Steps to Run and test the Program

- Navigate to the project workspace
- Open Command prompt
- Execute the Below Command to run the scraper main
```bash
python scraper.py
```
- Execute the Below Command to run the test cases
```bash
python test_scraper.py
```
