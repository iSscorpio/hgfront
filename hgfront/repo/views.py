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
    """
    List all repoistories linked to a project
    """
    project = get_object_or_404(Project, name_short__exact=slug)
    repos = Repo.objects.filter(project=project.id)
    is_auth = [project for project in Project.objects.all() if project.get_permissions(request.user).view_repos]
    return render_to_response('repos/repo_list.html', {'project':project, 'repos': repos, 'permissions':project.get_permissions(request.user), 'is_auth': is_auth})

@check_project_permissions('view_repos')
def repo_detail(request, slug, repo_name):
    from mercurial.hgweb.request import wsgiapplication
    from mercurial.hgweb.hgweb_mod import hgweb
    def make_web_app():
        return hgweb(str(settings.MERCURIAL_REPOS + slug + '/' + repo_name ))
    return HttpResponse(wsgiapplication(make_web_app))

@check_project_permissions('add_repos')
def repo_create(request, slug):
    """
        This function displays a form based on the model of the repo to authorised users
        who can create repos.  If the repo does not already exist in the project then it
        is created and the user is redirected there
    """
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
