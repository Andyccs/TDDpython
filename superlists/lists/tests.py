from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

from lists.views import home_page

class HomePageTest(TestCase):

	# Can we resolve the URL for the root of the site to a 
	# particular view function we've made
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	# Can we make this view function return some HTML which 
	# will get the functional test to pass?
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(),expected_html)

class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_display_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1',list=list_)
		Item.objects.create(text='itemey 2',list=list_)

		# Instead of calling the view function directly, we use the Django
		# test client, which is an attribute of Django TtestCase called
		# self.client. We tell it to .get the URL we're testing - it's 
		# actually a very similar API to the one that Selenium uses. 
		response = self.client.get('/lists/the-only-list-in-the-world/')

		# Instead of using the slightly annoying 
		# asserIn/response.content.decode() dance, Django provides the
		# assertContains method which knows how to deal with responses 
		# and the bytes of their content
		self.assertContains(response,'itemey 1')
		self.assertContains(response,'itemey 2')

class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'})

		# we check that one new Item has been saved to the database.
		# objects.count() is a shorthand for objects.all().count()
		self.assertEqual(Item.objects.count(), 1)
		# objects.first() is the same as doing objects.all()[0]
		new_item = Item.objects.first()
		# we check that the item's text is correct
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'})

		self.assertRedirects(response,'/lists/the-only-list-in-the-world/')

