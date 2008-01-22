from django.template import Context
from hgfront.project.models import Project

def num_projects(request):
    """
    This function returns the number of projects
    """
    return {'hgf_num_projects': Project.objects.all().count()}
