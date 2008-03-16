# General Libraries
# Django Libraries
from django.conf import settings
from django.conf.urls.defaults import *
# Project Libraries

urlpatterns = patterns('hgfront.member.views',
    url('^register/$','member_register', name='member-register'),
)
