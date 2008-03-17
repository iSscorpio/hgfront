# General Libraries
# Django Libraries
from django.conf import settings
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('hgfront.member.views',
    url(r'^register/$','member_register', name='member-register'),
    url(r'^login/$','member_login', name='member-login'),
    url(r'^logout/$','member_logout', name='member-logout'),
    url(r'^home/$','member_home', name='member-home'),
    url(r'^passwordreset/$','member_password', name='member-password'),
    url(r'^verifyusername/$','member_verifyusername', name='member-verifyusername'),
    url(r'^verifyuseremail/$','member_verifyuseremail', name='member-verifyuseremail'),
)
