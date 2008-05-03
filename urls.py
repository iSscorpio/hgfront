from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^admin/', include('core.django_docs.urls')),
    url(r'^admin/',include('django.contrib.admin.urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login-screen'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.HGFRONT_STATIC_PATH}, name='static-content'),
    url(r'^p/',include('project.urls'), name='projects-root'),
    url(r'^config/', include('core.config.urls'), name='config-root'),
    url(r'^u/',include('member.urls'), name='users-root'),
    url(r'^s/', include('search.urls'), name='search-root'),
    url(r'^r/', include('repo.urls'), name='repos-root'),
)

#urlpatterns += patterns('core.openidconsumer.views',
#    url(r'^openid/$', 'begin', name='openid'),
#    url(r'^openid/complete/$', 'complete', name='openid-complete'),
#    url(r'^openid/signout/$', 'signout', name='openid-signout'),
#)