#General Libraries
from mercurial import hg, ui, hgweb
import datetime, os
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.forms import RepoCreateForm
from hgfront.repo.models import Repo
from hgfront.project.decorators import check_project_permissions
from hgfront.queue.models import Message, Queue

@check_project_permissions('view_repos')
def repo_list(request, slug):
    """
    List all repoistories linked to a project
    """
    project = get_object_or_404(Project, name_short__exact=slug)
    repos = Repo.objects.filter(parent_project=project.id)
    return render_to_response('repos/repo_list.html',
        {
            'project': project,
            'repos': repos,
            'permissions': project.get_permissions(request.user)
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('view_repos')
def view_changeset(request, slug, repo_name, changeset='tip'):
    repo = Repo.objects.get(name_short__exact=repo_name)
    project = Project.objects.get(name_short__exact=slug)
    
    try:
        changeset_tags = repo.get_tags()
    except:
        changeset_tags = []
        
    try:
        changeset_branches = repo.get_branches()
    except:
        changeset_branches = []
    
    try:
        changeset_id = repo.get_changeset(changeset)
    except:
        changeset_id = []
        
    try:
        changeset_user = repo.get_changeset(changeset).user()
    except:
        changeset_user = []
        
    try:
        changeset_notes = repo.get_changeset(changeset).description()
    except:
        changeset_notes = []
        
    try:
        changeset_files = repo.get_changeset(changeset).files()
    except:
        changeset_files = []
        
    try:
        changeset_number = repo.get_changeset_number(changeset)
    except:
        changeset_number = []
    
    try:
        changeset_children = repo.get_next_changeset(changeset)
    except:
        changeset_children = []
        
    try:
        changeset_parents = repo.get_previous_changeset(changeset)
    except:
        changeset_parents = []
    
    return render_to_response('repos/repo_detail.html',
        {
            'changeset_tags': changeset_tags,
            'changeset_branches': changeset_branches,
            'changeset_id': changeset_id,
            'changeset_user': changeset_user,
            'changeset_notes': changeset_notes,
            'changeset_files': changeset_files,
            'changeset_number': changeset_number,
            'changeset_parents': changeset_parents,
            'changeset_children': changeset_children,
            'project': project,
            'repo': repo
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('add_repos')
def repo_create(request, slug):
    """
        This function displays a form based on the model of the repo to authorised users
        who can create repos.  If the repo does not already exist in the project then it
        is created and the user is redirected there
    """
    
    # Get the project from the database that we want to associate with
    project = get_object_or_404(Project, name_short__exact=slug)
    
    # Lets decide if we show the form or create a repo
    if request.method == "POST":
        # Were saving, so lets create our instance
        repo = Repo(parent_project=project, pub_date=datetime.datetime.now())
        form = RepoCreateForm(request.POST, instance=repo)
        # Lets check the form is valid
        if form.is_valid():
            form.save();
        # Return to the project view    
        return HttpResponseRedirect(reverse('project-detail',
            kwargs={
                'slug': slug,
                'repo_name':form.cleaned_data['name_short']
            })
        )
    else:
        form = RepoCreateForm()
    return render_to_response('repos/repo_create.html',
        {
            'form':form.as_table(),
            'project':project,
            'permissions':project.get_permissions(request.user)
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('add_repos')
def repo_manage(request, slug, repo_name):
    repo = Repo.objects.get(name_short = repo_name, parent_project__name_short = slug)
    if repo.create_hgrc():
        return HttpResponse('Created')
    else:
        return HttpResponse('Failed')
    
def repo_action(request, slug, repo_name, action):
    repo = Repo.objects.get(name_short = repo_name, parent_project__name_short = slug)
    u = ui.ui()
    r = hg.repository(u, repo.repo_directory())
    return HttpResponse('Foo Bar')
        
