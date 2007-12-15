from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url('^$','hgfront.repo.views.repo_list', name='repo-list'),
    url('^(?P<slug>\d+)/$', 'hgfront.repo.views.repo_detail', name='repo-detail'),
)
