# General Libraries
from mercurial import hg, ui, hgweb
import datetime
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Project Libraries
from hgfront.config.models import InstalledStyles
from hgfront.project.forms import *
from hgfront.project.models import Project, ProjectPermissionSet
from hgfront.project.decorators import check_project_permissions

def get_project_list(request):
    projects = [project for project in Project.objects.select_related()if project.get_permissions(request.user).view_project]
    return render_to_response('project/project_list.html', {'object_list':projects}, context_instance=RequestContext(request))

@check_project_permissions('view_project')
def get_project_details(request, slug):
    project = get_object_or_404(Project.objects.select_related(), name_short=slug)
    permissions = project.get_permissions(request.user)
    issues_shown = 10 #TODO: Move this either to settings.py or make it user configurabl
    issue_short_list = project.issue_set.select_related()[:issues_shown]
    return render_to_response('project/project_detail.html', {'project': project, 'permissions':permissions, 'issues':issue_short_list}, context_instance=RequestContext(request))

@login_required
def create_project_form(request):
    """
    This form shows in this order:
        1. Show the initial form with just name_short
        2. Check if the project already exists, if not show the second form
        3. Check to see if the name_long is in the request.POST keys (this needs a better check)
        4. Once the data is entered, save the form to the model
        5. Redirect to the project view
    """
    if request.method == "POST":
        if 'name_long' not in request.POST:
            form = NewProjectForm(request.POST)
            if form.is_valid():
                form_data = request.POST.copy()
                form_data['user_owner'] = request.user.username
                form_data['pub_date'] = datetime.datetime.now()
                form2 = NewProjectStep2(form_data)
                return render_to_response('project/project_create_step_2.html', {'form':form2, 'name_short':form.cleaned_data['name_short'], 'user_owner':request.user.username}, context_instance=RequestContext(request))
            else:
                return render_to_response('project/project_create.html', {'form':form,}, context_instance=RequestContext(request))
                
        else:
            form = NewProjectStep2(request.POST)
            if form.is_valid():
                style = InstalledStyles.objects.get(short_name__exact = form.cleaned_data['hgweb_style'])
                project = Project(
                    name_short = form.cleaned_data['name_short'],
                    name_long = form.cleaned_data['name_long'],
                    description_short = form.cleaned_data['description_short'],
                    description_long = form.cleaned_data['description_long'],
                    user_owner = request.user,
                    pub_date = datetime.datetime.now(),
                    hgweb_style = style
                ).save()
                request.user.message_set.create(message="The project has been added! Good luck on the project, man!")
                return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':form.cleaned_data['name_short']}))
            else:
                return render_to_response('project/project_create_step_2.html', {'form':form,}, context_instance=RequestContext(request))
    else:
        form = NewProjectForm()
        is_auth = bool(request.user.is_authenticated())
        return render_to_response('project/project_create.html', {'form':form, 'is_auth': is_auth}, context_instance=RequestContext(request))
 
@check_project_permissions('add_members')
def processjoinrequest(request, slug):
    project = get_object_or_404(Project.objects.select_related(), name_short = slug)
    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            permissionset = get_object_or_404(project.projectpermissionset_set.select_related(), user__username = form.cleaned_data['username'], owner_accepted = False)
            if form.cleaned_data['action'] == 'accept':
                project.accept_join_request(permissionset)
                request.user.message_set.create(message='%s was added to the project!' % form.cleaned_data['username'])
            elif form.cleaned_data['action'] == 'deny':
                permissionset.delete()
                request.user.message_set.create(message='the request from %s was denied' % form.cleaned_data['username'])
            return HttpResponseRedirect(project.get_absolute_url())
    return HttpResponse('Must be called with post and must be a valid username')
