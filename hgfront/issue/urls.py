from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url('^$','hgfront.issue.views.issue_list', name='issue-list'),
    url('^create/$','hgfront.issue.views.issue_create', name='issue-create'),
    url('^(?P<issue_id>\d+)/$', 'hgfront.issue.views.issue_detail', name='issue-detail'),
    url('^severity/(?P<group_by_value>[-\w]+)/$', 'hgfront.issue.views.issue_list', {'listed_by':'severity'}, name='issue-list-by-severity'),
    url('^type/(?P<group_by_value>[-\w]+)/$', 'hgfront.issue.views.issue_list', {'listed_by':'type'}, name='issue-list-by-type'),
    url('^status/(?P<group_by_value>[-\w]+)/$', 'hgfront.issue.views.issue_list', {'listed_by':'status'}, name='issue-list-by-status'),
)
