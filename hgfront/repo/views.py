#General Libraries
from mercurial import hg, ui, hgweb
# Django Libraries
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.forms import RepoCreateForm
from hgfront.repo.models import Repo
from hgfront.project.decorators import check_project_permissions

@check_project_permissions('view_repos')
def repo_list(request, slug):
   return HttpResponse("repo list")

@check_project_permissions('view_repos')
def repo_detail(request, slug, repo_name):
    project = get_object_or_404(Project, name_short__exact=slug)
    permissions = project.get_permissions(request.user)
    repo_db = get_object_or_404(Repo, repo_dirname__exact=repo_name)
    repo = hgweb.hgweb(str(settings.MERCURIAL_REPOS + project.name_short + '/' + repo_db.repo_dirname ))
    return HttpResponse(repo)

@check_project_permissions('add_repos')
def repo_create(request, slug):
    if request.method == "POST":
        form = RepoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('repo-detail', kwargs={'slug':slug,'repo_name':request.POST['repo_dirname']}))
    else:
        form = RepoCreateForm()
    is_auth = [project for project in Project.objects.all() if project.get_permissions(request.user).add_repos]
    project = get_object_or_404(Project, name_short__exact=slug)
    return render_to_response('repos/repo_create.html', {'form':form.as_table(), 'project':project, 'permissions':project.get_permissions(request.user), 'is_auth': is_auth})
