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

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^view/(?P<slug>[-\w]+)/$', 'object_detail', project_dict, name="project-detail"),                      
)