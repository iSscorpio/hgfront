from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_detail

from hgfront.project.models import Project, Repo

def get_project_details(request, slug):
    project = get_object_or_404(Project, shortname__exact=slug)
    repos = Repo.objects.all().filter(project__id=project.id)
    return render_to_response('project/project_detail.html', {'project': project, 'repos': repos})