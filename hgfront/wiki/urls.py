from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

# Generic Patterns
urlpatterns = patterns('',
    url(r'^/?$', 'hgfront.wiki.views.wiki_index', name="wiki-index"),
    url(r'^(?P<page_name>[-\w]+)/$', 'hgfront.wiki.views.wiki_page', name="wiki-page"),
    url(r'^edit/(?P<page_name>[-\w]+)/$', 'hgfront.wiki.views.wiki_edit', name="wiki-edit"),
)