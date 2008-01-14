# General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
# Project Libraries
from hgfront.config.models import InstalledStyles
from hgfront.project.forms import *
from hgfront.project.models import Project, ProjectPermissionSet
# Decorators
from hgfront.project.decorators import check_project_permissions

def get_project_list(request):
    projects = [project for project in Project.objects.all() if project.get_permissions(request.user).view_project]
    return render_to_response('project/project_list.html', {'object_list':projects}, context_instance=RequestContext(request))

@check_project_permissions('view_project')
def get_project_details(request, slug):
    project = get_object_or_404(Project, name_short=slug)
    permissions = project.get_permissions(request.user)
    issues_shown = 10 #TODO: Move this either to settings.py or make it user configurabl
    issue_short_list = project.issue_set.all()[:issues_shown]
    return render_to_response('project/project_detail.html', {'project': project, 'permissions':permissions, 'issues':issue_short_list}, context_instance=RequestContext(request))

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
                check = Project.objects.all().filter(name_short__exact = request.POST['name_short'])
                if check:
                    is_auth = bool(request.user.is_authenticated())
                    return render_to_response('project/project_create.html', {'form':form.as_table(), 'is_auth': is_auth, 'fail':'A Project with this name already exists'}, context_instance=RequestContext(request))
                else:
                    form_data = request.POST.copy()
                    form_data['user_owner'] = request.user.username
                    form_data['pub_date'] = datetime.datetime.now()
                    is_auth = bool(request.user.is_authenticated())
                    form = NewProjectStep2(form_data)
                    return render_to_response('project/project_create_step_2.html', {'form':form.as_table(), 'is_auth': is_auth, 'name_short':request.POST['name_short'], 'user_owner':request.user.username}, context_instance=RequestContext(request))
        else:
            user = User.objects.get(username__exact = request.POST['user_owner'])
            style = InstalledStyles.objects.get(short_name__exact = request.POST['hgweb_style'])
            project = Project(
                name_short = request.POST['name_short'],
                name_long = request.POST['name_long'],
                description_short = request.POST['description_short'],
                description_long = request.POST['description_long'],
                user_owner = user,
                pub_date = request.POST['pub_date'],
                hgweb_style = style
            ).save()
            return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':request.POST['name_short']}))
    else:
        form = NewProjectForm()
        is_auth = bool(request.user.is_authenticated())
        return render_to_response('project/project_create.html', {'form':form.as_table(), 'is_auth': is_auth}, context_instance=RequestContext(request))
 
