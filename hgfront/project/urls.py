from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

# Generic Patterns
urlpatterns = patterns('',
    url(r'^/?$', 'hgfront.project.views.get_project_list', name="project-list"),
    url(r'^create/$', 'hgfront.project.views.create_project_form', name="project-create"),
    url(r'^(?P<slug>[-\w]+)/$', 'hgfront.project.views.get_project_details', name="project-detail"),
)


# Issues
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/issues/', include('hgfront.issue.urls')),
    url(r'^(?P<slug>[-\w]+)/repos/', include('hgfront.repo.urls')),
)
