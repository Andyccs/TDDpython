from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # capture group, (.+), which will match any characters, up to the 
    # following /. The captured text will get passed to the view as 
    # an argument.
    url(r'^(\d+)/$', 'lists.views.view_list', 
    	name='view_list'),
    url(r'^(\d+)/add_item$', 'lists.views.add_item', name='add_item'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)
