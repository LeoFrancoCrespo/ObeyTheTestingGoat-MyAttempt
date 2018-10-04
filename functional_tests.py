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

        # invited to enter a to-do item straight away 
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # tries to put a task into a text box
        inputbox.send_keys('Buy peackock feathers')

        # page updates after pressing enter, 
        # lists that task in a to-do list table 
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1) 

        table = self.browser.find_element_by_id('id_lsit_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # The text box is still there inviting adding another item 
        self.fail('Finish the test!')




if __name__ == '__main__':
    unittest.main(warnings='ignore')

