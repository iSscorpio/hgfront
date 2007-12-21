# General Libraries
# Django Libraries
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('',
    url('^$','hgfront.issue.views.issue_list', name='issue-list'),
    url('^create/$','hgfront.issue.views.issue_create', name='issue-create'),
    url('^(?P<issue_id>\d+)/$', 'hgfront.issue.views.issue_detail', name='issue-detail'),
)
