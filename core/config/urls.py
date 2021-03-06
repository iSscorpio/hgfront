from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('core.config.views',
    url(r'^$', 'site_settings', name="site-config"),
    url(r'^(?P<app_label>[^/]+)/$', 'app_settings'),
)
