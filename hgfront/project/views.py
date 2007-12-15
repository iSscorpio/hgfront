from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from mercurial import hg, ui
from mercurial.hgweb.webcommands import *

from hgfront.project.forms import ProjectCreateForm
from hgfront.project.models import Project, ProjectPermissionSet

def get_project_list(request):
    projects = Project.objects.all().filter(is_private=0)
    return object_list(request, queryset=projects)

def get_project_details(request, slug):
    project = get_object_or_404(Project, shortname__exact=slug)
    #search for the specific permissions of a user
    try:
        permissions = ProjectPermissionSet.objects.get(user__id=request.user.id, project__id=project.id)
    except ProjectPermissionSet.DoesNotExist:
        #if we don't find them search for the default permissions of the project
        permission_list = ProjectPermissionSet.objects.filter(is_default=True, project__id=project.id)
        #if there were no default permissions for the project (alhtough there should always be one),
        #set the permissions to None. basically this should never happen but it's here for robustness
        if len(permission_list) > 0:
            permissions = permission_list[0]
        else:
            permissions = None
    return render_to_response('project/project_detail.html', {'project': project, 'permissions': permissions})

def create_project_form(request):
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hgfront/projects/' + request.POST['shortname'])
    else:
        form = ProjectCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('project/project_create.html', {'form':form, 'is_auth': is_auth})
 
