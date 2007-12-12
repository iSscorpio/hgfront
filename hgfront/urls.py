from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^project/',include('hgfront.project.urls')),
	url(r'^registration/',include('hgfront.registration.urls')),
)
