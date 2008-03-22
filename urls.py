from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^admin/',include('django.contrib.admin.urls'), name='admin'),
    url(r'^',include('hgfront.urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login-screen'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.HGFRONT_STATIC_PATH}, name='static-content')
)