# General Libraries
# Django Libraries
from django.conf import settings
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('hgfront.member.views',
    url('^register/$','member_register', name='member-register'),
    url('^login/$','member_login', name='member-login'),
    url('^logout/$','member_logout', name='member-logout'),
    url('^home/$','member_home', name='member-home'),
    url('^passwordreset/$','member_password', name='member-password'),
    url('^verifyusername/$','member_verifyusername', name='member-verifyusername'),
    url('^verifyuseremail/$','member_verifyuseremail', name='member-verifyuseremail'),
)
