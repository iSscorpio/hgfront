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
from hgfront.core.json_encode import json_encode
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.forms import RepoCreateForm
from hgfront.repo.models import *
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
    project = Project.objects.get(name_short__exact=slug)
    repo = Repo.objects.get(name_short__exact=repo_name, parent_project__exact = project)
    
    
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
        repo = Repo(
                    parent_project=project,
                    repo_created = True,
                    pub_date=datetime.datetime.now()
                )
        form = RepoCreateForm(request.POST, instance=repo)
        # Lets check the form is valid
        if form.is_valid():
            creation_method = int(form.cleaned_data['creation_method'])
            if creation_method==1:
                # We create the repo right away
                u = ui.ui()
                print repo.repo_directory()
                hg.repository(u, repo.repo_directory() + form.cleaned_data['name_short'] , create=True)
                form.cleaned_data['repo_created'] = True
                form.save();
            else:
                # We pass off to a queue event
                msg_string = {}
                
                msg_string['repo_name'] = form.cleaned_data['name_short']
                msg_string['project_name'] = str(form.cleaned_data['parent_project'].name_short)
                
                q = Queue.objects.get(name='repoclone')
                clone = simplejson.dumps(msg_string)
                msg = Message(message=clone, queue=q)
                msg.save()
                # Save the repo, save the world!
                form.cleaned_data['repo_created'] = False
                form.save()
        # Return to the project view
        
        if request.is_ajax():
            return HttpResponse(
                                "{'success': 'true', 'url': '" + reverse('project-detail', kwargs={'slug':slug}) + "', 'project': " + json_encode(project) + "}"
                                , mimetype="application/json")
        else:
            return HttpResponseRedirect(reverse('project-detail', kwargs={'slug': slug}))
            
    else:
        form = RepoCreateForm()
        
    if request.is_ajax():
        template = 'repos/repo_create_ajax.html'
    else:
        template = 'repos/repo_create.html'
    return render_to_response(template,
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
    
# Queue stuff
def check_allowed_methods(methods=['GET']):
    '''Convenient decorator that verifies that a view is being called with 
an allowed set of request methods and no others.
Returns HttpResponseForbidden if view is called with a disallowed method.'''
    def _decorator(view_func):
        def _wrapper(request, *args, **kwargs):
            if request.method in methods:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        _wrapper.__doc__ = view_func.__doc__
        _wrapper.__dict__ = view_func.__dict__
        return _wrapper
    return _decorator

# Queue Methods
@check_allowed_methods(['POST'])
def create_queue(request):
    # test post with
    # curl -i http://localhost:8000/createqueue/ -d name=default
    requested_name = request.POST.get('name', None)
    if requested_name is None:
        return HttpResponseForbidden()
    q = Queue(name=requested_name)
    q.save()
    return HttpResponse("", mimetype='text/plain')

@check_allowed_methods(['POST', 'DELETE'])
def delete_queue(request):
    # test post with
    # curl -i http://localhost:8000/deletequeue/ -d name=default
    requested_name = request.POST.get('name', None)
    if requested_name is None:
        return HttpResponseForbidden()
    try:
        q = Queue.objects.get(name=requested_name)
        if q.message_set.count() > 0:
            return HttpResponseNotAllowed()
        q.delete()
        return HttpResponse("", mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()

@check_allowed_methods(['POST'])
def purge_queue(request):
    # test post with
    # curl -i http://localhost:8000/purgequeue/ -d name=default
    requested_name = request.POST.get('name', None)
    if requested_name is None:
        return HttpResponseForbidden()
    try:
        q = Queue.objects.get(name=requested_name)
        q.message_set.all().delete()
        return HttpResponse("", mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()

@check_allowed_methods(['GET'])
def list_queues(request):
    # test post with
    # curl -i http://localhost:8000/listqueues/
    result_list = []
    for queue in Queue.objects.all():
        result_list.append(queue.name)
    return HttpResponse(simplejson.dumps(result_list), mimetype='application/json')

#
# Message methods - all of these will be operating on messages against a queue...
#

@check_allowed_methods(['GET'])
def get(request, queue_name, response_type='text'):
    # test count with
    # curl -i http://localhost:8000/q/default/
    # curl -i http://localhost:8000/q/default/json/
    
    # print "GET queue_name is %s" % queue_name
    q = None
    # pre-emptive queue name checking...
    try:
        q = Queue.objects.get(name=queue_name)
    except Queue.DoesNotExist:
        return HttpResponseNotFound()
    #
    msg = q.message_set.pop()
    if msg:
        u = ui.ui()
        repo = simplejson.loads(msg.message)
        message_id = msg.id
        project = Project.objects.get(name_short__exact = repo['project_name'])
        clone = Repo.objects.get(name_short__exact=repo['repo_name'], parent_project__exact=project)
        clone.repo_created = True
        clone.save()
        hg.clone(u, str(clone.default_path), str(clone.repo_directory()), True)
        message = Message.objects.get(id=message_id, queue=q.id)
        message.delete()
        
    return HttpResponse(simplejson.dumps(msg.message), mimetype='application/json')

#@check_allowed_methods(['POST'])
def clear_expirations(request, queue_name):
    # test count with
    # curl -i http://localhost:8000/q/default/clearexpire/
    # @TODO: This should only work with a POST as the following code changes data
    try:
        Message.objects.clear_expirations(queue_name)
        return HttpResponse("", mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()

@check_allowed_methods(['GET'])
def count(request, queue_name, response_type='text'):
    # test count with
    # curl -i http://localhost:8000/q/default/count/
    # curl -i http://localhost:8000/q/default/count/json/
    try:
        q = Queue.objects.get(name=queue_name)
        num_visible = q.message_set.filter(visible=True).count()
        if response_type == 'json':
            msg_dict = {"count":"%s" % num_visible}
            return HttpResponse(simplejson.dumps(msg_dict), mimetype='application/json')
        else:
            return HttpResponse("%s" % num_visible, mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()

@check_allowed_methods(['POST', 'DELETE'])
def delete(request, queue_name):
    # test post with
    # curl -i http://localhost:8000/q/default/delete/ -d message_id=1
    #print "deleting: %s" % message_id
    message_id=request.POST['message_id']
    try:
        q = Queue.objects.get(name=queue_name)
        msg = q.message_set.get(pk=message_id)
        msg.delete()
        return HttpResponse("OK", mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()
    except Message.DoesNotExist:
        return HttpResponseNotFound()

@check_allowed_methods(['POST'])
def put(request, queue_name):
    # test post with
    # curl -i http://localhost:8000/q/default/put/ -d message=hello
    try:
        q = Queue.objects.get(name=queue_name)
        msg = Message(message=request.POST['message'], queue=q)
        msg.save()
        return HttpResponse("OK", mimetype='text/plain')
    except Queue.DoesNotExist:
        return HttpResponseNotFound()