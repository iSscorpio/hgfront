from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from hgfront.project.models import Project
def project_edit(request, slug):
    return HttpResponse('editing of project %s' % slug)
    #TODO: implement this

def project_delete(request, slug):
    return HttpResponse('deletion of project %s' % slug)
    #TODO: implement this
