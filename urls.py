from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^admin/',include('django.contrib.admin.urls'), name='admin'),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login-screen'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.HGFRONT_STATIC_PATH}, name='static-content'),
    url(r'^p/',include('project.urls'), name='projects-root'),
    url(r'^config/', include('config.urls'), name='config-root'),
    url(r'^u/',include('member.urls'), name='users-root'),
    url(r'^s/', include('search.urls'), name='search-root'),
    url(r'^r/', include('repo.urls'), name='repos-root'),
)