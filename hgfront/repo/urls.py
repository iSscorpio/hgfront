from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url('^$','hgfront.repo.views.repo_list', name='repo-list'),
    url('^(?P<repo_id>\w+)/$', 'hgfront.repo.views.repo_detail', name='repo-detail'),
)
