# General Libraries
# DJango Libraries
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Project Libraries

urlpatterns = patterns('',
	url(r'^projects/',include('hgfront.project.urls')),
	url(r'^config/', include('hgfront.config.urls')),
	url(r'^member/',include('hgfront.member.urls')),
	url(r'^search/', include('hgfront.search.urls')),
)
#static content
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.HGFRONT_STATIC_PATH})
)
