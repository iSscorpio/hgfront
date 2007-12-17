from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from hgfront.repo.forms import RepoCreateForm
from hgfront.repo.models import Project

def repo_list(request, slug):
   return HttpResponse("repo list") 

def repo_detail(request, slug, repo_name):
   return HttpResponse("repo detail") 

def repo_create(request, slug):
    if request.method == "POST":
        form = RepoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hgfront/projects/' + slug + '/repos/' + request.POST['name'])
    else:
        form = RepoCreateForm()
    is_auth = [project for project in Project.objects.all() if project.get_permissions(request.user).add_repos]
    return render_to_response('repos/repo_create.html', {'form':form, 'project':slug, 'is_auth': is_auth})