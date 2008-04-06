# General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.conf import settings
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('hgfront.repo.views',
    url(r'^$','repo_list', name='repo-list'),
    url(r'^create/$','repo_create', name='repo-create'),
    url(r'^(?P<repo_name>[-\w]+)/$', 'view_changeset', name='view-tip'),
    url(r'^(?P<repo_name>[-\w]+)/pull/$','repo_pull_request', name='repo-pull-request'),
    url(r'^(?P<repo_name>[-\w]+)/changeset/(?P<changeset>[-\w]+)/$', 'view_changeset', name='view-changeset'),
)

urlpatterns += patterns('hgfront.repo.views',
    url(r'^q/createqueue/$', 'create_queue'), #post 'name' of queue
    url(r'^q/deletequeue/$', 'delete_queue'), #post 'name' of queue
    url(r'^q/purgequeue/$', 'purge_queue'),   #post 'name' of queue
    url(r'^q/listqueues/$', 'list_queues'),
    url(r'^q/(?P<queue_name>\w+)/clearexpire/$', 'clear_expirations'),
    url(r'^q/(?P<queue_name>\w+)/count/json/$', 'count', {"response_type":"json"}),
    url(r'^q/(?P<queue_name>\w+)/count/$', 'count', {"response_type":"text"}),
    url(r'^q/(?P<queue_name>\w+)/$', 'pop_queue'),

)