from django.db.models import Q
from django.shortcuts import render_to_response
from hgfront.project.models import Project
from hgfront.repo.models import Repo
from hgfront.issue.models import Issue
# Create your views here.

def search_results(request):
    """
    Search Function
    """
    query = request.POST.get('search_term', '')
    print "Query: %s" % query
    if query:
        qset_projects = (
            Q(name_short__icontains=query) |
            Q(name_long__icontains=query) |
            Q(description_short__icontains=query) |
            Q(description_long__icontains=query)
        )
        qset_repos = (
            Q(repo_name__icontains=query) |
            Q(repo_dirname__icontains=query) |
            Q(repo_description__icontains=query)
        )
        qset_issues = (
            Q(title__icontains=query) |
            Q(body__icontains=query)
        )
        results_projects = Project.objects.filter(qset_projects).distinct()
        results_repos = Repo.objects.filter(qset_repos).distinct()
        results_issues = Issue.objects.filter(qset_issues).distinct()
    else:
        results_projects = "There are no results for projects."
        results_repos = "There are no results for repos."
        results_issues = "There are no results for issues."
        
    return render_to_response("search/search_results.html", {
        "projects": results_projects,
        "repos": results_repos,
        "issues": results_issues,
        "search_term": query
    })
            
