import datetime
from random import randint

from django.template import Context
from hgfront.project.models import Project

def site_options(request):
    return dict([
                ('hgf_site_name', Project.project_options.site_name),
                ('hgf_site_owner', Project.project_options.site_owner),
            ])


def project_stats(request):
    """
    This function returns the number of projects
    """
    num_projects = Project.objects.all().count()
    past24 = datetime.datetime.now() - datetime.timedelta(days=1)
    
    return dict([
            ('hgf_num_projects', num_projects),
            ('hgf_num_projects_last_24_hours', Project.objects.filter(pub_date__gt=past24).count()),
            # Needs fixed as throws error on fresh install
            #('hgf_random_project', [if num_projects: Project.objects.all()[randint(0, num_projects-1)] else: return {'error':'There are currently no projects'}]),
        ])
