from django.test import LiveServerTestCase
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import WebDriverException
import time 

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(1)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # trying to get onto homepage
        self.browser.get(self.live_server_url)

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
        # page updates after pressing enter, 
        # lists that task in a to-do list table 
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # now will add more items to the list 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        
        # User 01 comes around and tries to do user 01 things 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # does user01 have their own url for their list
        user01_list_url = self.browser.current_url
        self.assertRegex(user01_list_url, '/lists/.+')

        ## We are going to go ahead and close user01's session so  
        ## we can see what happens with user02
        self.browser.quit()
        self.browser = webdriver.Firefox() 

        # user02 comes around and visits a home page, check that it's empty
        self.browser.get(self.live_server_url) 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # user02 comes in and does some stuff 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # check user02 has their own URL
        user02_list_url = self.browser.find_element_by_id('id_new_item')
        self.assertRegex(user02_list_url, '/lists/.+')
        self.assertNotEqual(user01_list_url, user02_list_url)

        # do a check that user01's stuff still isn't here 
        page_text = self.browser.find_element_by_tag_name('body').textcl
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

