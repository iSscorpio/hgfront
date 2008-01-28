from hgfront.wiki.models import Page
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import hgfront.markdown as markdown

def view_page(request, slug, page_name):
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return render_to_response("wiki/create.html", {"project":slug, "page_name": page_name})
        
    return render_to_response("wiki/page.html", {"project":slug,"page_name":page_name, "content":markdown.markdown(page.content)})
    
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
    
    return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/" + page_name + "/")
