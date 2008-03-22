# General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.conf import settings
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('hgfront.repo.views',
    url('^$','repo_list', name='repo-list'),
    url('^create/$','repo_create', name='repo-create'),
    url('^(?P<repo_name>[-\w]+)/$', 'view_changeset', name='view-tip'),
    url('^(?P<repo_name>[-\w]+)/changeset/(?P<changeset>[-\w]+)/$', 'view_changeset', name='view-changeset'),
    url('^(?P<repo_name>[-\w]+)/manage/$', 'repo_manage', name='repo-manage'),
    url('^(?P<repo_name>[-\w]+)/action/(?P<action>[-\w]+)$', 'repo_action', name='repo-action'),
)
