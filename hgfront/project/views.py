# General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
# Project Libraries
from hgfront.project.forms import ProjectCreateForm
from hgfront.project.models import Project, ProjectPermissionSet
# Decorators
from hgfront.project.decorators import check_project_permissions

def get_project_list(request):
    projects = [project for project in Project.objects.all() if project.get_permissions(request.user).view_project]
    return render_to_response('project/project_list.html',{'object_list':projects}, context_instance=RequestContext(request))

@check_project_permissions('view_project')
def get_project_details(request, slug):
    project = get_object_or_404(Project, name_short=slug)
    permissions = project.get_permissions(request.user)
    issues_shown = 10 #TODO: Move this either to settings.py or make it user configurabl
    issue_short_list = project.issue_set.all()[:issues_shown]
    return render_to_response('project/project_detail.html', {'project': project, 'permissions':permissions, 'issues':issue_short_list}, context_instance=RequestContext(request))

def create_project_form(request):
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':request.POST['name_short']}))
    else:
        form = ProjectCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('project/project_create.html', {'form':form.as_table(), 'is_auth': is_auth}, context_instance=RequestContext(request))
 
