from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'search.views.search_results', name="search-results"),
)
