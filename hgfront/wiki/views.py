from hgfront.wiki.models import Page, PageChange
from hgfront.project.models import Project
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import hgfront.markdown as markdown

def view_page(request, slug, page_name):
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return render_to_response("wiki/create.html", {"project":slug, "page_name": page_name})
    page = Page.objects.get(name=page_name)
    project = Project.objects.get(name_short__exact=slug)
    return render_to_response("wiki/page.html", {"project":project, "page": page, "content":markdown.markdown(page.content)})
    
def edit_page(request, slug, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        content = page.content
    except Page.DoesNotExist:
        content = ""
    return render_to_response("wiki/edit.html", {"project":slug, "page_name": page_name, "content":content})
    
def save_page(request, slug, page_name):

    content = request.POST['content']

    try:
        page = Page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    page.save()
    if request.POST['change']:
        changeset = PageChange(page_id=page, change_message = request.POST['change'])
        changeset.save()
    
    return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/" + page_name + "/")
    
def view_changes(request, slug, page_name):
    project = Project.objects.get(name_short__exact=slug)
    page = Page.objects.get(name=page_name)
    return render_to_response("wiki/changes.html", {"project":project, "page":page, "changesets": page.changesets()})
