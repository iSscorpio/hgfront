from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'hgfront.search.views.search_results', name="search-results"),
)
