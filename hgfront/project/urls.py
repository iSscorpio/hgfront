# General Libraries
# Django Libraries
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
# Project Libraries

# Generic Patterns
urlpatterns = patterns('',
    url(r'^$', 'hgfront.project.views.get_project_list', name="project-list"),
    url(r'^create/$', 'hgfront.project.views.create_project_form', name="project-create"),
    url(r'^(?P<slug>[-\w]+)/$', 'hgfront.project.views.get_project_details', name="project-detail"),
    url(r'^(?P<slug>[-\w]+)/process_join_request/$', 'hgfront.project.views.process_join_request', name="project-process-join-request"),
    url(r'^(?P<slug>[-\w]+)/join/$', 'hgfront.project.views.join_project', name="project-join-project"),
    url(r'^(?P<slug>[-\w]+)/backup/$', 'hgfront.project.views.create_project_backup', name="create-backup"),
)


# Issues
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/issues/', include('hgfront.issue.urls')),
    url(r'^(?P<slug>[-\w]+)/repos/', include('hgfront.repo.urls')),
    url(r'^(?P<slug>[-\w]+)/wiki/',include('hgfront.wiki.urls')),
)
