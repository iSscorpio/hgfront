from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('core.django_docs.views',
    ('^doc/django/$', 'index'),
    ('^doc/django/([^/]*)/$', 'doc_reader'),
)