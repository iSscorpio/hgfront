from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from hgfront.project.models import Project, Repo

project_dict = {
    'queryset': Project.objects.all(),
    'slug_field': 'shortname',
    'extra_context':  {
        'repos': Repo.objects.all().distinct()
    }
}

# Generic Patterns
urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^/?$', 'object_list', project_dict, name="project-list"),
    url(r'^(?P<slug>[-\w]+)/$', 'object_detail', project_dict, name="project-detail"),                      
)

# View Patterns
urlpatterns += patterns('hgfront.project.views',
    url(r'^(?P<slug>[-\w]+)/edit/$', 'project_edit', project_dict, name="project-edit"),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'project_delete', project_dict, name="project-delete"),                      
)
# Issues
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/issues/', include('hgfront.issue.urls')),
)
