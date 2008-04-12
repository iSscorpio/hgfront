# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response

from project.models import Project, ProjectPermissionSet, ProjectNews

def landing_page(request):
    
    latest_projects = Project.objects.all()[:10]
    
    return render_to_response('landing/index.html', {
                'latest_projects': latest_projects
            })