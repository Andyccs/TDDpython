from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

		# waiting for page to complete loading before it tries to do anything,
		# but it's not perfect. 
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do',self.browser.title)

		# It is used as a reminder to finish the test
		self.fail('Finish the test!')

		# She is invited to enter a to-do item straight away

		# She types "Buy peacok feathers" into a text box (Edith's hobby
		# is tying fly-fishing lures)

		# When she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do lists

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edutg us very methodical)

		# The page updates again, and now shows both items on her lists

		# Edith wonders whether the site will remember her list. The she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits the URL - her to-do list is still there.

		# Satisfied, she goes back to sleep

# That's how Python script checks if it's been executed from the command line
# , rather than just imported by another script
if __name__ == '__main__':
	unittest.main(warnings='ignore')