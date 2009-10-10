# General Libraries
# Django Libraries
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
# Project Libraries

admin.autodiscover()

# Generic Patterns
urlpatterns = patterns('project.views',
    url(r'^$', 'get_project_list', name="project-list"),
    url(r'^verifyprojectshortname/$','project_verifyprojectshortname', name='project-verifyprojectshortname'),
    url(r'^create/$', 'create_project_form', name="project-create"),
    url(r'^(?P<slug>[-\w]+)/$', 'get_project_details', name="project-detail"),
    url(r'^(?P<slug>[-\w]+)/process_join_request/$', 'process_join_request', name="project-process-join-request"),
    url(r'^(?P<slug>[-\w]+)/join/$', 'join_project', name="project-join-project"),
    url(r'^(?P<slug>[-\w]+)/news/$', 'project_news', name="project-add-news"),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'project_delete', name="project-delete"),
)


# Issues
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/i/', include('issue.urls')),
    url(r'^(?P<slug>[-\w]+)/r/', include('repo.urls')),
    url(r'^(?P<slug>[-\w]+)/b/', include('backup.urls')),
)
