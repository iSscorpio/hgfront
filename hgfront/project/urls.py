from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from hgfront.project.models import Project, Repo

project_list_dict = {
    'queryset':Project.objects.all(),
}

# Generic Patterns
urlpatterns = patterns('',
    url(r'^/?$', 'django.views.generic.list_detail.object_list', project_list_dict, name="project-list"),
    url(r'^(?P<slug>[-\w]+)/$', 'hgfront.project.views.get_project_details', name="project-detail"),                      
)


# Issues
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/issues/', include('hgfront.issue.urls')),
)
