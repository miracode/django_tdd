from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    # special methods which run before and after each test
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        # element returns element, raising exception if not found
        table = self.browser.find_element_by_id('id_list_table')
        # element*s* returns a list (which may be empty)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # New visitor would like to visit the homepage
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to ender a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # User types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When user hits enter, the page updates and pages lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        user_list_url = self.browser.current_url
        self.assertRegexpMatches(user_list_url, '/list/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting user to add another item
        # user enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # A new user comes to the site

        ## Make new browser session
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # The new user visits the home page.  There is no sighn of old user's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # New user starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # New user gets his own unique URL
        new_user_list_url = self.browser.current_url
        self.assertRegexpMatches(new_user_list_url, '/list/.+')
        self.assertNotEqual(new_user_list_url, user_list_url)

        # Again, there is no sign of old user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they go to sleep
