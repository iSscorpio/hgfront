import datetime
from random import randint

from django.template import Context
from core.libs.json_libs import json_encode

from project.models import Project
from repo.models import Repo
from member.models import Member

def json_output(request):
    
    if request.user.is_anonymous():
        member = "null"
    else :
        try:
            member = Member.members.filter(user = request.user).values('openid', 'member_displayname', 'member_homepage', 'member_gtalk', 'member_msn', 'member_jabber', 'member_bio', 'member_lat', 'member_lng')
        except:
            member = "null"
        
    site_options = {
        'site_name': Project.project_options.site_name,
        'site_owner': Project.project_options.site_owner,
        'repo_directory': Project.project_options.repository_directory,    
    }
    
    json_vars = json_encode(
        {
            'user': member,
            'site_options': site_options,
        }
    )
    return dict([
                 ('json_vars', json_vars),
            ])

def site_options(request):
    return dict([
                ('hgf_site_name', Project.project_options.site_name),
                ('hgf_site_owner', Project.project_options.site_owner),
                ('hgf_logged_in_user', request.user.username),
            ])


def project_stats(request):
    """
    This function returns the number of projects
    """
    num_projects = Project.projects.all().count()
    past24 = datetime.datetime.now() - datetime.timedelta(days=1)
    
    return dict([
            ('hgf_num_projects', num_projects),
            ('hgf_num_projects_last_24_hours', Project.projects.filter(modified_date__gt=past24).count()),
            # Needs fixed as throws error on fresh install
            #('hgf_random_project', [if num_projects: Project.objects.all()[randint(0, num_projects-1)] else: return {'error':'There are currently no projects'}]),
        ])

def repo_stats(request):
    """
    This function returns the number of repos
    """
    past24 = datetime.datetime.now() - datetime.timedelta(days=1)
    
    return dict([
            ('hgf_num_repos', Repo.objects.all().count()),
            ('hgf_num_repos_last_24_hours', Repo.objects.filter(local_creation_date__gt=past24).count()),
        ])
