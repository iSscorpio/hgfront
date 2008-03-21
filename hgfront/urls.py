# General Libraries
# DJango Libraries
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Project Libraries

urlpatterns = patterns('',
	url(r'^p/',include('hgfront.project.urls')),
	url(r'^config/', include('hgfront.config.urls')),
	url(r'^u/',include('hgfront.member.urls')),
	url(r'^s/', include('hgfront.search.urls')),
	url(r'^q/', include('hgfront.queue.urls')),
)
