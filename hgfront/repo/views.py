#General Libraries
from mercurial import hg, ui, hgweb
import datetime, os
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.forms import RepoCreateForm
from hgfront.repo.models import Repo
from hgfront.project.decorators import check_project_permissions

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
        changeset_children = repo.get_next_changeset(changeset)
    except:
        changeset_children = []
        
    try:
        changeset_parents = repo.get_previous_changeset(changeset)
    except:
        changeset_parents = []
    
    return render_to_response('repos/repo_detail.html',
        {
            'tags': repo.get_tags(),
            'branches': repo.get_branches(),
            'changeset_id': repo.get_changeset(changeset),
            'changeset_user': repo.get_changeset(changeset).user(),
            'changeset_notes': repo.get_changeset(changeset).description(),
            'changeset_files': repo.get_changeset(changeset).files(),
            'changeset_number': repo.get_changeset_number(changeset),
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
    project = get_object_or_404(Project, name_short__exact=slug)
    if request.method == "POST":
        repo = Repo(parent_project=project, pub_date=datetime.datetime.now())
        form = RepoCreateForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="The repo has been added! Now start putting code in!")
            return HttpResponseRedirect(reverse('project-detail',
                kwargs={
                    'slug': slug,
                    'repo_name':request.POST['name_short']})
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
    
#def local_clone(request, slug, repo_name):
#    if request.method = "POST":
        
