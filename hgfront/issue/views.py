# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
from django.core.urlresolvers import reverse
from django.template import RequestContext
# Project Libraries
from hgfront.config.models import SiteOptions
from hgfront.issue.models import *
from hgfront.issue.forms import IssueCreateForm
from hgfront.project.models import Project
from hgfront.project.decorators import check_project_permissions
from hgfront.shortcuts import get_object_related_or_404

@check_project_permissions('view_issues')
def issue_list(request, slug):
    """Returns a list of isses that belong to the project identified by `slug`
    Also, this accepts querystring variables:

    `page` - which page we want to view
    
    `completed` - do we want to see completed or uncompleted issues. A value
    of `yes` means we want it to show the completed ones, anything else matches
    uncompleted issues

    Apart from these two querystring variables, it also accepts filter variables
    that act just as if you gave them as keyword arguments for the filter function.
    So an example querystring for this view might look like

    ?page=1&issue_sev__slug=minor&issue_type__slug=bug&completed=no
    """
    i = SiteOptions.objects.get(option_key__exact = 'issues_per_page')
    issues_per_page = int(i.option_value)

    #read the page variable in the querystring to determine which page we are at
    page = request.GET['page'] if request.GET.has_key('page') else 1
    try:
        page = int(page)-1
    except ValueError:
        page = 0

    project = get_object_related_or_404(Project, name_short = slug)
    issues = project.issue_set.select_related()

    #check if we're filtering the issues by completed and if we are, filter the selection
    if request.GET.has_key('completed'):
        issues = issues.filter(finished_date__isnull = False if request.GET['completed']=='yes' else True)

    #modify the querydict so it doesn't have completed and page in it
    GET_copy = request.GET.copy()
    if GET_copy.has_key('completed'):
        del GET_copy['completed']
    if GET_copy.has_key('page'):
        del GET_copy['page']

    #filter the issues by what's left
    issues = issues.filter(**dict([(str(key),str(value)) for key,value in GET_copy.items()]))

    #initialize the pagination
    paginator = ObjectPaginator(issues, issues_per_page)
    try:
        issues = paginator.get_page(page)
    except InvalidPage:
        issues = []

    #generate the list of pages for the template
    pages = []
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
        }, context_instance=RequestContext(request)
    )
    #TODO: Implement advanced filtering in the sidebar (kind of like the filtering the django admin has)

@check_project_permissions('view_issues')
def issue_detail(request, slug, issue_id):
    """Returns the details of the issue identified by `issue_id`"""
    project = get_object_related_or_404(Project, name_short = slug)
    issue = get_object_related_or_404(Issue, id = issue_id)
    return render_to_response('issue/issue_detail.html',
        {
            'project':project,
            'issue':issue,
            'permissions':project.get_permissions(request.user),
        }, context_instance=RequestContext(request)
    )

@check_project_permissions('add_issues')
def issue_create(request, slug):
    """
    This view displays a form based on a new issue
    """
    project = get_object_related_or_404(Project, name_short=slug)
    if request.method == "POST":
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            # Let's set the values that we don't get explicitly from the form
            issue.project = project
            issue.pub_date = datetime.datetime.now()
            issue.user_posted = request.user
            issue.save()
            # Let's send a message of success to the user if the user isn't anonymous
            if request.user.is_authenticated():
                request.user.message_set.create(message="The issue has been added. Let's hope someone solves it soon!")
            return HttpResponseRedirect(reverse('issue-detail', kwargs={'slug':slug,'issue_id':issue.id}))
    else:
        form = IssueCreateForm()
    return render_to_response('issue/issue_create.html', 
        {
            'form':form, 
            'project':project, 
            'permissions':project.get_permissions(request.user)
        }, context_instance=RequestContext(request)
    )
