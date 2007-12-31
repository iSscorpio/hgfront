# General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('',
    url('^$','hgfront.repo.views.repo_list', name='repo-list'),
    url('^create/$','hgfront.repo.views.repo_create', name='repo-create'),
    url('^(?P<repo_name>\w+)/$', 'hgfront.repo.views.repo_detail', name='repo-detail'),
)
