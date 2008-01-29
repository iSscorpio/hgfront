from django.conf.urls.defaults import *

urlpatterns = patterns('hgfront.config.views',
    (r'^$', 'site_settings'),
    (r'^(?P<app_label>[^/]+)/$', 'app_settings'),
)
