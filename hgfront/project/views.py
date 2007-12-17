from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from mercurial import hg, ui, hgweb

from hgfront.project.forms import ProjectCreateForm
from hgfront.project.models import Project, ProjectPermissionSet

def get_project_list(request):
    projects = [project for project in Project.objects.all() if project.get_permissions(request.user).can_view_project]
    return render_to_response('project/project_list.html',{'object_list':projects})

def get_project_details(request, slug):
    project = get_object_or_404(Project, name_short=slug)
    permissions = project.get_permissions(request.user)
    return render_to_response('project/project_detail.html', {'project': project, 'permissions':permissions})

def create_project_form(request):
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':request.POST['name_short']}))
    else:
        form = ProjectCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('project/project_create.html', {'form':form, 'is_auth': is_auth})
 
