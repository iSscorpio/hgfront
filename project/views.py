# General Libraries
from mercurial import hg, ui, hgweb
import datetime, os, string
from time import strftime
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
# Project Libraries
from core.json_response import JsonResponse
from backup.models import ProjectBackup
from core.json_encode import json_encode
from project.forms import *
from project.models import Project, ProjectPermissionSet, ProjectNews
from project.decorators import check_project_permissions
from issue.models import Issue
from member.models import Member

# Experimental Caching stuff
from django.core.cache import cache
CACHE_EXPIRES = 5 * 60 # 5 minutes
# End caching stuff

def get_project_list(request):
    projects = [project for project in Project.projects.all() if project.get_permissions(request.user).view_project]
    project_news = ProjectNews.news_items.filter(frontpage=True, authorised=True).order_by('-pub_date')[:2]
    #user_can_request_to_join = ProjectPermissionSet.objects.filter(project=project, user__id=request.user.id).count()<1 and request.user.is_authenticated() and request.user != project.user_owner
    
    if request.is_ajax():
        template = 'project/project_list_ajax.html'
    else:
        template = 'project/project_list.html'
    
    return render_to_response(template,
        {
            'view_title': "All Projects",
            'projects': projects,
            'project_news': project_news,
            'json_output': json_encode({'projects' : projects,}),
            #'user_can_request_to_join':user_can_request_to_join
        }, context_instance=RequestContext(request)
    )

def get_project_details(request, slug):
    #cache_key = "hgfrontcache%s" % slug
    #object_list = cache.get(cache_key)
    #if not object_list:
    #    project = get_object_or_404(Project.objects.select_related(), name_short=slug)
    #    cache.set(cache_key, project, CACHE_EXPIRES)

    project = get_object_or_404(Project.projects.select_related(), project_id=slug)
    permissions = project.get_permissions(request.user)
    
    backups = ProjectBackup.objects.filter(parent_project__exact=project).order_by('-created')
    
    issue_short_list = project.issue_set.select_related()[:Issue.issue_options.issues_per_page]
    user_can_request_to_join = ProjectPermissionSet.objects.filter(project=project, user__id=request.user.id).count()<1 and request.user.is_authenticated() and request.user != project.project_manager
    
    if request.is_ajax():
        template = 'project/project_detail_ajax.html'
    else:
        template = 'project/project_detail.html'
    
    return render_to_response(template,
        {
            'project': project,
            'permissions':permissions,
            'issues':issue_short_list,
            'backups': backups,
            'user_can_request_to_join':user_can_request_to_join,
            'json_output': json_encode({'project' : project, 'issues': issue_short_list}),
        }, context_instance=RequestContext(request)
    )

def create_project_form(request):
    """
    Form to create a new project
    """
    
    # First we check to see the site has been set up, otherwise we throw the user to the config screen
    if not bool(os.path.isdir(Project.project_options.repository_directory)):
        request.user.message_set.create(message="The site has not been set up yet.  Log in as your admin user and create your settings!")
        return HttpResponseRedirect(reverse('site-config'))
    
    if request.is_ajax():
        template ='project/project_create_ajax.html'
    else:
        template = 'project/project_create.html'
    
    # Lets check if this form is being shown or processed
    if request.method == "POST":
        # We're processing the form, so lets create the instance
        form = NewProjectForm(request.POST, auto_id=False)
        # The form is correct, lets proceeed.
        if form.is_valid():
            # Lets check the user has conformed to a sites T&C's
            if form.cleaned_data['t_and_c'] == True:
                # Create the project instance
                project = Project(
                    project_id = string.lower(form.cleaned_data['project_id']),
                    project_name = form.cleaned_data['project_name'],
                    short_description = form.cleaned_data['short_description'],
                    full_description = form.cleaned_data['full_description'],
                    project_manager = request.user,
                    hgweb_style = form.cleaned_data.get('hgweb_style', ''),
                    project_icon = form.cleaned_data['project_icon'],
                )
                # Ok, we're all good, so lets save.
                project.save()
                # We'll tell the user that there site has been saved
                request.user.message_set.create(message=_("The project " + form.cleaned_data['project_name'] + " has been created"))
                if request.is_ajax():
                    return HttpResponse(
                                        "{'success': 'true', 'url': '" + reverse('project-detail', kwargs={'slug':form.cleaned_data['project_id']}) + "', 'project': " + json_encode(project) + "}"
                                        , mimetype="application/json")
                else:
                    return HttpResponseRedirect(reverse('project-detail', kwargs={'slug': form.cleaned_data['project_id']}))
        else:
            return render_to_response(template,
                {
                    'form':form.as_table(),
                }, context_instance=RequestContext(request)
            )
        #return HttpResponseRedirect(reverse('project-detail', kwargs={'slug':form.cleaned_data['name_short']}))
    else:
        form = NewProjectForm()
        is_auth = request.user.is_authenticated()
        
        return render_to_response(template,
            {
                'form':form.as_table(),
                'is_auth': is_auth
            }, context_instance=RequestContext(request)
        )
        
def project_delete(request, slug):
    project = get_object_or_404(Project.projects.select_related(), project_id=slug)
    try:
        project.delete()
        request.user.message_set.create(message=_("The project " + project.project_name + " has been deleted"))
        if request.is_ajax():
            retval = (
                {
                    'success':'true',
                    'url': reverse('project-detail', kwargs={'slug':slug}),
                },
            )
            return JsonResponse(retval)
        else:
            return HttpResponseRedirect(reverse('project-detail', kwargs={'slug': slug}))
    except:
        request.user.message_set.create(message=_("The repository " + repo.display_name + " failed to be deleted"))
        return HttpResponseRedirect(reverse('project-detail', kwargs={'slug': slug}))
        
 
def process_join_request(request, slug):
    project = get_object_or_404(Project.projects.select_related(), name_short = slug)
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
    project = get_object_or_404(Project.projects.select_related(), name_short = slug)
    if request.user.is_authenticated():
        permissionset, created = ProjectPermissionSet.projects.get_or_create(is_default=False, user=request.user, project=project)
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
        
def project_news(request, slug):
    project = get_object_or_404(Project.projects.select_related(), name_short = slug)
    if request.method == 'POST' and request.user.is_authenticated():
        form = ProjectNewsForm(request.POST)
        if form.is_valid():
            newsitem = ProjectNews.projects.get_or_create(parent_project=project, news_title=form.cleaned_data['news_title'], news_body=form.cleaned_data['news_body'], pub_date=datetime.datetime.now(), published=form.cleaned_data['published'], frontpage=form.cleaned_data['frontpage'], authorised=form.cleaned_data['authorised'])
            newsitem.save()
            return HttpResponseRedirect(project.get_absolute_url())
        else:
            return form.as_table()
    else:
        form = ProjectNewsForm()
        
        if request.is_ajax():
            template ='project/project_news_create_ajax.html'
        else:
            template = 'project/project_news_create.html'
            
        return render_to_response(template,
            {
                'form':form.as_table(),
            }, context_instance=RequestContext(request)
        )

def project_verifyprojectshortname(request):
    project_id = request['project_id']  
    try:
        check = Project.projects.get(project_id__exact=project_id)
    except Project.DoesNotExist:
        check = False
    
    if check:
        return HttpResponse('false')
    else:
        return HttpResponse('true')