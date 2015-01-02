from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	# we use a variable called new_item_text, which will either 
	# hold the POST contents, or the empty string

	if request.method =='POST':
		# .objects.create is a neat shorthand for creating a new 
		# Item, without needing to call .save()
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')

	items = Item.objects.all()
	return render(request,'home.html',{'items':items})