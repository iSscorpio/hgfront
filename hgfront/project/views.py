# General Libraries
from mercurial import hg, ui, hgweb
import datetime, os, string
from time import strftime
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Project Libraries
from hgfront.backup.models import ProjectBackup
from hgfront.project.forms import *
from hgfront.project.models import Project, ProjectPermissionSet, ProjectNews
from hgfront.project.decorators import check_project_permissions
from hgfront.issue.models import Issue

# Experimental Caching stuff
from django.core.cache import cache
CACHE_EXPIRES = 5 * 60 # 5 minutes
# End caching stuff

def get_project_list(request):
    projects = [project for project in Project.objects.select_related()if project.get_permissions(request.user).view_project]
    project_news = ProjectNews.objects.filter(frontpage=True, authorised=True).order_by('-pub_date')[:2]
    #user_can_request_to_join = ProjectPermissionSet.objects.filter(project=project, user__id=request.user.id).count()<1 and request.user.is_authenticated() and request.user != project.user_owner
    
    return render_to_response('project/project_list.html',
        {
            'projects': projects,
            'project_news': project_news,
            #'user_can_request_to_join':user_can_request_to_join
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('view_project')
def get_project_details(request, slug):
    #cache_key = "hgfrontcache%s" % slug
    #object_list = cache.get(cache_key)
    #if not object_list:
    #    project = get_object_or_404(Project.objects.select_related(), name_short=slug)
    #    cache.set(cache_key, project, CACHE_EXPIRES)

    project = get_object_or_404(Project.objects.select_related(), name_short=slug)
    permissions = project.get_permissions(request.user)
    
    backups = ProjectBackup.objects.filter(parent_project__exact=project).order_by('-created')
    
    issue_short_list = project.issue_set.select_related()[:Issue.issue_options.issues_per_page]
    user_can_request_to_join = ProjectPermissionSet.objects.filter(project=project, user__id=request.user.id).count()<1 and request.user.is_authenticated() and request.user != project.user_owner
    return render_to_response('project/project_detail.html',
        {
            'project': project,
            'permissions':permissions,
            'issues':issue_short_list,
            'backups': backups,
            'user_can_request_to_join':user_can_request_to_join
        }, context_instance=RequestContext(request)
    )

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
    
    if not bool(os.path.isdir(Project.project_options.repository_directory)):
        return HttpResponseRedirect(reverse('site-config'))
    
    if request.method == "POST":
        if 'name_long' not in request.POST:
            form = NewProjectForm(request.POST)
            if form.is_valid():
                form_data = request.POST.copy()
                form_data['user_owner'] = request.user.username
                form_data['pub_date'] = datetime.datetime.now()
                form2 = NewProjectStep2(form_data)
                return render_to_response('project/project_create_step_2.html',
                    {
                        'form':form2,
                        'name_short':string.lower(form.cleaned_data['name_short']),
                        'user_owner':request.user.username
                    }, context_instance=RequestContext(request)
                )
            else:
                return render_to_response('project/project_create.html',
                    {
                        'form':form,
                    }, context_instance=RequestContext(request)
                )
                
        else:
            form = NewProjectStep2(request.POST)
            if form.is_valid():
                project = Project(
                    name_short = string.lower(form.cleaned_data['name_short']),
                    name_long = form.cleaned_data['name_long'],
                    description_short = form.cleaned_data['description_short'],
                    description_long = form.cleaned_data['description_long'],
                    user_owner = request.user,
                    pub_date = datetime.datetime.now(),
                    hgweb_style = form.cleaned_data.get('hgweb_style', '')
                ).save()
                request.user.message_set.create(message="The project has been added! Good luck on the project, man!")
                return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':form.cleaned_data['name_short']}))
            else:
                return render_to_response('project/project_create_step_2.html',
                    {
                        'form':form,
                    }, context_instance=RequestContext(request)
                )
    else:
        form = NewProjectForm()
        is_auth = bool(request.user.is_authenticated())
        return render_to_response('project/project_create.html',
            {
                'form':form,
                'is_auth': is_auth
            }, context_instance=RequestContext(request)
        )
 
@check_project_permissions('add_members')
def process_join_request(request, slug):
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

def join_project(request, slug):
    project = get_object_or_404(Project.objects.select_related(), name_short = slug)
    if request.user.is_authenticated():
        permissionset, created = ProjectPermissionSet.objects.get_or_create(is_default=False, user=request.user, project=project)
        if created:
            permissionset.user_accepted = True
            permissionset.owner_accepted = False
            permissionset.save()
        else:
            return HttpResponse('You are already either in the project or waiting to be accepted or invited')
        request.user.message_set.create(message='You have requested to join this project!')
        return HttpResponseRedirect(project.get_absolute_url())
    else:
        return HttpResponse('You must register or login to join a project')
        
def add_project_news(request, slug):
    project = get_object_or_404(Project.objects.select_related(), name_short = slug)
    if request.method == 'POST' and request.user.is_authenticated():
        form = ProjectNewsForm(request.POST)
        if form.is_valid():
            newsitem = ProjectNews.objects.get_or_create(parent_project=project, news_title=form.cleaned_data['news_title'], news_body=form.cleaned_data['news_body'], pub_date=datetime.datetime.now(), published=form.cleaned_data['published'], frontpage=form.cleaned_data['frontpage'], authorised=form.cleaned_data['authorised'])
            newsitem.save()
            return HttpResponseRedirect(project.get_absolute_url())
        else:
            return form
    else:
        form = ProjectNewsForm()
        return render_to_response('project/project_news_create.html',
            {
                'form':form
            }, context_instance=RequestContext(request)
        )

def project_verifyprojectshortname(request):
    name_short = request['name_short']  
    try:
        check = Project.objects.get(name_short__exact=name_short)
    except Project.DoesNotExist:
        check = False
    
    if check:
        return HttpResponse('false')
    else:
        return HttpResponse('true')