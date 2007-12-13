from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^projects/',include('hgfront.project.urls')),
	url(r'^issues/',include('hgfront.issue.urls')),
	url(r'^registration/',include('registration.urls')),
)
