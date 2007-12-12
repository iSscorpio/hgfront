from django import template
from digitalspaghetti.blog.models import *
from hgfront.project.models import Project

register = template.Library()

@register.inclusion_tag("project/list_all_projects.html")
def list_all_projects(limit=0):
    """This will list all public projects.  Takes an optional limiter"""
    if limit == 0:
        projects = Project.objects.all().filter(private__exact=0).distinct()
    else:
        projects = Project.objects.all().filter(private__exact=0).distinct()[:limit]
    return {'project': projects}