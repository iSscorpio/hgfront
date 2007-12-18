# General Libraries
# Django Libraries
from django import template
# Project Libraries
from hgfront.issue.models import *
from hgfront.project.models import Project

register = template.Library()

@register.inclusion_tag("issue/tags/list_all_issues.html")
def list_all_issues(limit=0):
    """This will list all issues.  Takes an optional limiter"""
    if limit == 0:
        issues = Issue.objects.all().distinct()
    else:
        issues = Issue.objects.all().distinct()[:limit]
    return {'issues': issues}

@register.inclusion_tag("issues/tags/list_by_severity.html")
def list_by_severity(sev):
    """This will show all issues linked to severity"""
    issues = Issue.objects.all().filter(issue_sev=sev)
    return {'issues': issues}

@register.inclusion_tag("issues/tags/list_by_type.html")
def list_by_type(type):
    """This will show all issues linked to a type"""
    issues = Issue.objects.all().filter(issue_type=type)
    return {'issues': issues}