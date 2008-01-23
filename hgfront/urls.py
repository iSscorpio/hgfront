# General Libraries
# DJango Libraries
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Project Libraries

urlpatterns = patterns('',
	url(r'^projects/',include('hgfront.project.urls')),
	url(r'^config/', include('hgfront.config.urls')),
	url(r'^registration/',include('registration.urls')),
	url(r'^search/', include('hgfront.search.urls')),
	url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),
)
#static content
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.HGFRONT_STATIC_PATH})
)
