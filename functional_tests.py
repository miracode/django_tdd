from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    # special methods which run before and after each test
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # New visitor would like to visit the homepage
        self.browser.get('http://localhost:8000')

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

        import time
        time.sleep(10)

        # element returns element, raising exception if not found
        table = self.browser.find_element_by_id('id_list_table')
        # element*s* returns a list (which may be empty)
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table")

        # There is still a text box inviting user to add another item
        # user enters "Use peacock feathers to make a fly"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

        # User wonders whether the site will remember her list.  She then sees
        # that the site has generated a unique URL for her -- there is some
        # explanitory text to that effect

        # She visits that URL - her to-do list is still there.

        # Satisfied she goes back to sleep

if __name__ == '__main__':
    unittest.main()
