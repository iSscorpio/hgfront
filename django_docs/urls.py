from django.conf.urls.defaults import *

urlpatterns = patterns('django_docs.views',
    ('^doc/django/$', 'index'),
    ('^doc/django/([^/]*)/$', 'doc_reader'),
)