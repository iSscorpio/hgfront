# General Libraries
# Django Libraries
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
# Project Libraries

# Generic Patterns
urlpatterns = patterns('',
    url(r'^(?P<page_name>[-\w]+)/$', 'hgfront.wiki.views.view_page', name="wiki-page"),
    url(r'^(?P<page_name>[-\w]+)/edit/$', 'hgfront.wiki.views.edit_page', name="wiki-edit"),
    url(r'^(?P<page_name>[-\w]+)/save/$', 'hgfront.wiki.views.save_page', name="wiki-save"),
)
