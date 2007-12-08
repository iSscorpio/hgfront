from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^admin/', include('django.contrib.admin.urls')),
    url(r'^accounts/', include('hgfront.registration.urls')),
)
