import datetime
from random import randint

from django.template import Context
from hgfront.project.models import Project

def project_stats(request):
    """
    This function returns the number of projects
    """
    num_projects = Project.objects.all().count()
    past24 = datetime.datetime.now() - datetime.timedelta(days=1)
    
    return dict([
            ('hgf_num_projects', num_projects),
            ('hgf_num_projects_last_24_hours', Project.objects.filter(pub_date__gt=past24).count()),
            ('hgf_random_project', Project.objects.all()[randint(0, num_projects-1)]),
        ])
