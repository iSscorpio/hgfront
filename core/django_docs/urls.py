from django.conf.urls.defaults import *

urlpatterns = patterns('core.django_docs.views',
    ('^doc/django/$', 'index'),
    ('^doc/django/([^/]*)/$', 'doc_reader'),
)