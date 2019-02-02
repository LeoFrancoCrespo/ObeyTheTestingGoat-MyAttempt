from selenium import webdriver
import unittest 

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # notices title of page is To-Do
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # user is invited to enter a to-do item 

        # user enters "item 1" into the text box

        # user hits enter, page updates, and page lists 
        # "1: item 1" as an item in the list 

        # user enters "item 2" into the the text box 

        # user hits enter, page updates, page lists
        # "1: item 1"
        # "2: item 2" 

        # user gets a unique url specific for that list 

        
if __name__ == '__main__':
    unittest.main(warnings='ignore')