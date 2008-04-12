from wiki.models import Page, PageChange
from project.models import Project
from project.decorators import check_project_permissions
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

@check_project_permissions('view_wiki')
def view_page(request, slug, page_name):
    project = get_object_or_404(Project, name_short=slug)
    try:
        page = Page.objects.get(name=page_name, parent_project=project)
    except Page.DoesNotExist:
        return render_to_response("wiki/create.html", {"project":project, "page_name": page_name}, context_instance=RequestContext(request))
    else:
        return render_to_response("wiki/page.html", {"project":project, "page": page}, context_instance=RequestContext(request))
    
@check_project_permissions('edit_wiki')
def edit_page(request, slug, page_name):
    project = get_object_or_404(Project, name_short=slug)
    try:
        page = Page.objects.get(name=page_name, parent_project=project)
    except Page.DoesNotExist:
        content = ""
    else:
        content = page.content
    return render_to_response("wiki/edit.html", {"project":project, "page_name": page_name, "content":content}, context_instance=RequestContext(request))
    
@check_project_permissions('edit_wiki')
def save_page(request, slug, page_name):
    project = get_object_or_404(Project, name_short=slug)
    content = request.POST['content']
    try:
        page = Page.objects.get(name=page_name, parent_project=project)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content, parent_project=project)
    page.save()
    if request.POST['change']:
        changeset = PageChange(page_id=page, change_message = request.POST['change'])
        changeset.save()
    return HttpResponseRedirect(page.get_absolute_url())
    
@check_project_permissions('view_wiki')
def view_changes(request, slug, page_name):
    project = get_object_or_404(Project, name_short=slug)
    page = Page.objects.get(name=page_name, parent_project=project)
    return render_to_response("wiki/changes.html", {"project":project, "page":page, "changesets": page.changesets()}, context_instance=RequestContext(request))
