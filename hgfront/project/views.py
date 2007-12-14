from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.newforms import ModelForm

from hgfront.project.models import Project, Repo

def get_project_list(request):
    projects = Project.objects.all().filter(is_private=0)
    return object_list(request, queryset=projects)

def get_project_details(request, slug):
    project = get_object_or_404(Project, shortname__exact=slug)
    return render_to_response('project/project_detail.html', {'project': project})


class ProjectCreateForm(ModelForm):
    class Meta:
        model=Project

#def create_project_form(request):
#    ProjectFormClass = forms.models.form_for_model(Project)
#    form = ProjectFormClass()
#    return form 