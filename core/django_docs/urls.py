from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('core.django_docs.views',
    ('^django/$', 'index'),
    ('^django/([^/]*)/$', 'doc_reader'),
)