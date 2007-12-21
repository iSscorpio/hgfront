# General Libraries
# Django Libraries
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
from django.core.urlresolvers import reverse
# Project Libraries
from hgfront.issue.models import *
from hgfront.project.models import Project
from hgfront.project.decorators import check_project_permissions

@check_project_permissions('view_issues')
def issue_list(request, slug):
    """Returns a list of isses that belong to the project identified by `slug`
    Also, this accepts querystring variables:

    `page` - which page we want to view

    `severity` - by which severity we want the issues filtered

    `type` - by which type we want the issues filtered

    `status` - by which status we want the issues filtered

    `completed` - do we want to see completed or uncompleted issues. A value
    of `yes` means we want it to show the completed ones, anything else matches
    uncompleted issues
    """
    issues_per_page = 20 #TODO: move this to settings.py later on

    #read the page variable in the querystring to determine which page we are at
    page = request.GET['page'] if request.GET.has_key('page') else 1
    try:
        page = int(page)-1
    except ValueError:
        page = 0

    project = get_object_or_404(Project, name_short = slug)
    issues = project.issue_set.all()

    #check if we're filtering the issues by anything and if we are, filter the selection
    if request.GET.has_key('severity'):
        issues = issues.filter(issue_sev__slug = request.GET['severity'])
    if request.GET.has_key('type'):
        issues = issues.filter(issue_type__slug = request.GET['type'])
    if request.GET.has_key('status'):
        issues = issues.filter(issue_status__slug = request.GET['status'])
    if request.GET.has_key('completed'):
        completed = True if request.GET['completed']=='yes' else False
        issues = [issue for issue in issues if issue.completed() == completed]

    #initialize the pagination
    paginator = ObjectPaginator(issues, issues_per_page)
    try:
        issues = paginator.get_page(page)
    except InvalidPage:
        issues = []
    pages = []

    #generate the list of pages for the template
    if len(paginator.page_range) > 1:
        for page_number in paginator.page_range:
            new_query_dict = request.GET.copy()
            new_query_dict['page'] = page_number
            pages.append((page_number, new_query_dict.urlencode()))
    
    return render_to_response('issue/issue_list.html',
        {
            'project':project,
            'issue_list':issues,
            'permissions':project.get_permissions(request.user),
            'pages':pages,
            'current_page':page+1
        }
    )
    #TODO: Implement advanced filtering in the sidebar (kind of like the filtering the django admin has)

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
