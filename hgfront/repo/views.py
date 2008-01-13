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
from hgfront.config.models import InstalledStyles, InstalledExtensions
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
    return render_to_response('repos/repo_list.html', {'project':project, 'repos': repos, 'permissions':project.get_permissions(request.user), 'is_auth': is_auth}, context_instance=RequestContext(request))

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
    project = get_object_or_404(Project, name_short__exact=slug)
    if request.method == "POST":
        repo = Repo(project=project, pub_date=datetime.datetime.now())
        form = RepoCreateForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('repo-detail', kwargs={'slug':slug,'repo_name':request.POST['repo_dirname']}))
    else:
        form = RepoCreateForm()
    is_auth = [project for project in Project.objects.all() if project.get_permissions(request.user).add_repos]
    return render_to_response('repos/repo_create.html', {'form':form.as_table(), 'project':project, 'permissions':project.get_permissions(request.user), 'is_auth': is_auth}, context_instance=RequestContext(request))

def create_hgrc(project_name, repo_name):
    """This function outputs a hgrc file within a repo's .hg directory, for use with hgweb"""
    repo = Repo.objects.get(repo_dirname__exact=repo_name)
    c = User.objects.get(username__exact=repo.repo_contact)
    s = InstalledStyles.objects.get(short_name = repo.hgweb_style)
    directory = os.path.join(settings.MERCURIAL_REPOS, project_name, repo.repo_dirname)
       
    hgrc = open(os.path.join(directory, '.hg/hgrc'), 'w')
    hgrc.write('[paths]\n')
    hgrc.write('default = %s\n\n' % repo.repo_url)
    hgrc.write('[web]\n')
    hgrc.write('style = %s\n' % s.short_name)
    hgrc.write('description = %s\n' % repo.repo_description)
    hgrc.write('contact = %s <%s>\n' % (c.username, c.email))
    a = 'allow_archive = '
    if repo.offer_zip:
        a += 'zip '
    if repo.offer_tar:
        a += 'gz '
    if repo.offer_bz2:
        a += 'bz2'
    hgrc.write(a + '\n\n')
    hgrc.write('[extensions]\n')
    for e in repo.active_extensions.all():
        hgrc.write('hgext.%s = \n' % e.short_name)
    hgrc.close()
    return True


@check_project_permissions('add_repos')
def repo_manage(request, slug, repo_name):
    if bool(create_hgrc(slug, repo_name)):
        HttpResponse('Created')
    else:
        HttpResponse('Failed')
    
