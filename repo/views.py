#General Libraries
from mercurial import hg, ui, hgweb, commands, util, streamclone
from mercurial.node import bin, hex
from mercurial.hgweb import protocol
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
from core.json_encode import json_encode
from django.utils.translation import ugettext as _
# Project Libraries
from core.json_response import JsonResponse
from project.models import Project
from repo.forms import RepoCreateForm
from repo.models import Repo
from repo.queue import Queue, Message
from repo.decorators import check_allowed_methods
from project.decorators import check_project_permissions

@check_project_permissions('view_repos')
def repo_list(request, slug):
    """
    List all repoistories linked to a project
    """
    project = get_object_or_404(Project, project_id__exact=slug)
    repos = Repo.objects.filter(local_parent_project=project.id)
    return render_to_response('repos/repo_list.html',
        {
            'project': project,
            'repos': repos,
            'permissions': project.get_permissions(request.user)
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('view_repos')
def view_changeset(request, slug, repo_name, changeset='tip'):
    project = Project.projects.get(project_id__exact=slug)
    repo = Repo.objects.get(directory_name__exact=repo_name, local_parent_project__exact = project)
    
    cmd = request.GET.get('cmd','')
    if cmd:
        if cmd == 'heads':
            #u = ui.ui()
            #loc = hg.repository(u, repo.repo_directory)
            #resp = " ".join(map(hex, loc.heads())) + "\n"
            #return HttpResponse(resp, mimetype='application/mercurial-0.1')
            return HttpResponse('Not yet implemented')
    else:
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

def repo_create(request, slug):
    """
        This function displays a form based on the model of the repo to authorised users
        who can create repos.  If the repo does not already exist in the project then it
        is created and the user is redirected there
    """
    
    # Get the project from the database that we want to associate with
    project = get_object_or_404(Project, project_id__exact=slug)
    
    if request.is_ajax():
        template = 'repos/repo_create_ajax.html'
    else:
        template = 'repos/repo_create.html'
    
    # Lets decide if we show the form or create a repo
    if request.method == "POST":
        # Were saving, so lets create our instance
        repo = Repo(
                    local_parent_project=project,
                    created=True,
                    local_manager = request.user
                )
        form = RepoCreateForm(request.POST, instance=repo)
        
        # Lets check the form is valid
        if form.is_valid():
            creation_method = str(form.cleaned_data['creation_method'])
            if creation_method== "New":
                # We create the repo right away
                u = ui.ui()
                hg.repository(u, project.project_directory + str(form.cleaned_data['directory_name']), create=True)
                form.cleaned_data['created'] = True
                form.save();
            else:
                # We pass off to a queue event
                msg_string = {}
                
                msg_string['directory_name'] = form.cleaned_data['directory_name']
                msg_string['local_parent_project'] = project.project_id
                
                q = Queue.objects.get(name='repoclone')
                clone = simplejson.dumps(msg_string)
                msg = Message(message=clone, queue=q)
                msg.save()
                # Save the repo, save the world!
                form.cleaned_data['created'] = False
                form.save()
            
            request.user.message_set.create(message=_("The repository " + form.cleaned_data['display_name'] + " has been queued"))
            if request.is_ajax():
                retval = (
                    {'success':'true', 'url':reverse('project-detail', kwargs={'slug':slug}),},
                )
                return JsonResponse(retval)
            else:
                return HttpResponseRedirect(reverse('project-detail', kwargs={'slug': slug}))
        else:
            # Return to the project view
            return render_to_response(template,
                {
                    'form':form.as_table(),
                    'project':project,
                    'permissions':project.get_permissions(request.user)
                }, context_instance=RequestContext(request)
            )
    else:
        form = RepoCreateForm()
    return render_to_response(template,
        {
            'form':form.as_table(),
            'project':project,
            'permissions':project.get_permissions(request.user)
        }, context_instance=RequestContext(request)
    )
    
def repo_delete(request, slug, repo_name):
    project = get_object_or_404(Project, project_id__exact=slug)
    repo = Repo.objects.get(directory_name__exact=repo_name, local_parent_project__exact = project)
    try:
        repo.delete()
        request.user.message_set.create(message=_("The repository " + repo.display_name + " has been deleted"))
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

@check_project_permissions('add_repos')
def repo_manage(request, slug, repo_name):
    repo = Repo.objects.get(directory_name__exact=repo_name, local_parent_project__exact = project)
    if repo.create_hgrc():
        return HttpResponse('Created')
    else:
        return HttpResponse('Failed')
    
def repo_pull_request(request, slug, repo_name):
    repo = Repo.objects.get(directory_name__exact = repo_name, local_parent_project__project_id__exact = slug)
    # We pass off to a queue event
    msg_string = {}
                
    msg_string['directory_name'] = repo.directory_name
    msg_string['local_parent_project'] = repo.local_parent_project.project_id
                
    q = Queue.objects.get(name='repoupdate')
    update = simplejson.dumps(msg_string)
    msg = Message(message=update, queue=q)
    try:
        msg.save()
        request.user.message_set.create(message="Your repository update has been queued!")
    except:
        request.user.message_set.create(message="The repository queue has failed!")
    return HttpResponseRedirect(reverse('view-tip', kwargs={'slug': slug, 'repo_name':repo_name}))
    
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

#@check_allowed_methods(['GET'])
def pop_queue(request, queue_name):
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
        message = simplejson.loads(msg.message)
        project = Project.projects.get(project_id__exact = message['local_parent_project'])
        repo = Repo.objects.get(directory_name__exact=message['directory_name'], local_parent_project__exact=project)
        
        if (queue_name == 'repoclone'):
            try:
                hg.clone(u, str(repo.default_path), repo.repo_directory, True)
                repo.created = True
                
                for (path, dirs, files) in os.walk(repo.repo_directory):
                    for file in files:
                        filename = os.path.join(path, file)
                        repo.folder_size += os.path.getsize(filename)
                
                repo.save()
                m = Message.objects.get(id=msg.id, queue=q.id)
                m.delete()
                project.save()
                return HttpResponse('success')
            except:
                return HttpResponse('failed')
        elif (queue_name == 'repoupdate'):
            location = hg.repository(u, repo.repo_directory)
            try:
                commands.pull(u, location, str(repo.default_path), rev=['tip'], force=True, update=True)
                for (path, dirs, files) in os.walk(repo.repo_directory):
                    for file in files:
                        filename = os.path.join(path, file)
                        repo.folder_size += os.path.getsize(filename)
                repo.save()
                m = Message.objects.get(id=msg.id, queue=q.id)
                m.delete()
                project.save()
                return HttpResponse('success')
            except:
                return HttpResponse('fail')
    return HttpResponse('void')

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
