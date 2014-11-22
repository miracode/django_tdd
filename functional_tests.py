from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    # special methods which run before and after each test
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # New visitor would like to visit the homepage
        self.browser.get('http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is invited to ender a to-do item straight away

        # User types "Buy peacock feathers" into a text box

        # When user hits enter, the page updates and pages lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting user to add another item
        # user enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # User wonders whether the site will remember her list.  She then sees
        # that the site has generated a unique URL for her -- there is some 
        # explanitory text to that effect

        # She visits that URL - her to-do list is still there.

        # Satisfied she goes back to sleep

if __name__ == '__main__':
    unittest.main()
