# General Libraries
# Django Libraries
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

# Project Libraries

urlpatterns = patterns('issue.views',
    url(r'^$','issue_list', name='issue-list'),
    url(r'^(?P<issue_id>\d+)/$', 'issue_detail', name='issue-detail'),
    url(r'^(?P<issue_id>\d+)/edit/$', 'issue_edit', name='issue-edit'),
    url(r'^create/$','issue_create', name='issue-create'),
)
