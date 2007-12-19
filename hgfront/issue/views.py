# General Libraries
# Django Libraries
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
# Project Libraries
from hgfront.issue.models import *
from hgfront.project.models import Project
from hgfront.project.decorators import check_project_permissions

@check_project_permissions('view_issues')
def issue_list(request, slug, listed_by=None, group_by_value=None):
    """Returns a list of isses that belong to the project identified by `slug`
    If `listed_by` and `group_by_value` are specified, it will display a filtered
    list. Example:

       hgfront/projects/hgfront/issues/severity/extreme
    This would mean that `listed_by`='severity' and `group_by_value`='extreme' """
    project = get_object_or_404(Project, name_short = slug)
    if listed_by is None:
        issues = project.issue_set.all()
    else:
        if listed_by == 'severity':
            issues = project.issue_set.filter(issue_sev__slug = group_by_value)
        if listed_by == 'type':
            issues = project.issue_set.filter(issue_type__slug = group_by_value)
        if listed_by == 'status':
            issues = project.issue_set.filter(issue_status__slug = group_by_value)
    return render_to_response('issue/issue_list.html',
        {
            'project':project,
            'issue_list':issues,
            'permissions':project.get_permissions(request.user),
            'listed_by':listed_by,
            'group_by_value':group_by_value,
        }
    )
    #TODO: Implement pagination (ugh)

@check_project_permissions('view_issues')
def issue_detail(request, slug, issue_id):
    """Returns the details of the issue identified by `issue_id`"""
    project = get_object_or_404(Project, name_short = slug)
    issue = get_object_or_404(Issue, id = issue_id)
    return render_to_response('issue/issue_detail.html',
        {
            'project':project,
            'issue':issue,
            'permissions':project.get_permissions(request.user),
        }
    )

@check_project_permissions('add_issues')
def issue_create(request, slug):
    return HttpResponse('Create issue')
