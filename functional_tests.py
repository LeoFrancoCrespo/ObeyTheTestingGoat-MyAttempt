from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import unittest 

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # trying to get onto homepage
        self.browser.get('http://localhost:8000')

        # notice the title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

