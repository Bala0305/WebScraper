import unittest
import os
import json
from bs4 import BeautifulSoup
from scraper import scrap_data_from_web,extract_product_info,write_to_json,find_median


class TestSleepAidScraper(unittest.TestCase):

    def test_scrap_data_from_web(self):
        # Test case for existing HTML file
        html_file_name = "test_data.html"
        expected_result = BeautifulSoup("<html><body><p>This is a test HTML content.</p></body></html>", 'lxml')
        with open(html_file_name, 'w', encoding='utf-8') as test_html:
            test_html.write("<html><body><p>This is a test HTML content.</p></body></html>")
        self.assertEqual(scrap_data_from_web(html_file_name).prettify(), expected_result.prettify())
        os.remove(html_file_name)

        # print("Success: test_scrap_data_from_web passed. \n")

    def test_extract_product_info(self):
        # Create a sample BeautifulSoup object with HTML content
        html_content = """
        <div class="oct-teaser__contents-panel--main-content">
            <h3 class="oct-teaser__title">Bach Rescue Remedy Night Dropper 10ml - Flower Essences for Natural Night's Sleep</h3>
            <p class="oct-teaser__productPrice">£9.5</p>
            <div class="oct-reviews__optionalText"><a aria-label="4.5 out of 5"></a></div>
            <a class = "oct-teaser__title-link" href="./products/Bach Rescue Night Dropper - 10ml - Boots.html">Link to Product 1</a>
        </div>
        """
        soup = BeautifulSoup(html_content, 'lxml')

        # Call the extract_product_info function
        product_list = extract_product_info(soup)

        # Check if product details are extracted correctly
        self.assertEqual(len(product_list), 1)
        self.assertEqual(product_list[0]['Title'], "Bach Rescue Remedy Night Dropper 10ml - Flower Essences for Natural Night's Sleep")
        self.assertEqual(product_list[0]['Price'], 9.5)
        self.assertEqual(product_list[0]['Price_Unit'], '£')
        self.assertEqual(product_list[0]['Rating'], 4.5)
        self.assertEqual(product_list[0]['Short_Desc'], "Bach Rescue Remedy Night Dropper 10ml - Flower Essences for Natural Night's Sleep")  # Assuming extract_short_description_and_size returns empty string
        self.assertEqual(product_list[0]['Page_Size'], 1799)  # Assuming extract_short_description_and_size returns 0 KB

        # print("Success: test_extract_product_info passed. \n")

    def test_write_to_json(self):
        # Define sample product details
        product_list_details = [
            {'Title': 'Product 1', 'Price': 10.99},
            {'Title': 'Product 2', 'Price': 15.99},
            {'Title': 'Product 3', 'Price': 20.99}
        ]

        # Define the name of the JSON file
        json_file_name = "test_product_details.json"

        # Call the function with sample data
        write_to_json(product_list_details, json_file_name)

        current_working_directory = os.getcwd()
        output_folder_path = os.path.join(current_working_directory,"output")
        output_json_file_path = os.path.join(output_folder_path,json_file_name)

        # Check if the JSON file was created successfully
        self.assertTrue(os.path.exists(output_json_file_path))

        # Check if the JSON file contains the expected data
        with open(output_json_file_path, 'r') as json_file:
            data = json.load(json_file)
            self.assertIn('Products', data)
            self.assertIn('Median', data)
            self.assertEqual(len(data['Products']), len(product_list_details))

        os.remove(output_json_file_path) # Clean up: remove the created JSON file
        # print("Success: test_write_to_json passed. \n")

    def test_find_median(self):
        # Test case with odd number of prices
        price_list = [10.0, 20.0, 30.0, 40.0, 50.0]
        expected_median = 30.0
        self.assertEqual(find_median(price_list), expected_median)

        # Test case with even number of prices
        price_list = [10.0, 20.0, 30.0, 40.0]
        expected_median = 25.0
        self.assertEqual(find_median(price_list), expected_median)

        # Test case with a single price
        price_list = [25.0]
        expected_median = 25.0
        self.assertEqual(find_median(price_list), expected_median)
        # print("Success: test_find_median passed. \n")

if __name__ == '__main__':
    unittest.main()
