from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^admin/',include('django.contrib.admin.urls')),
    url(r'^hgfront/',include('hgfront.urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login-screen')
)

from hgfront import htpasswdutils
htpasswdutils.monkeypatch_user_model()

