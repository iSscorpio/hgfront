# General Libraries
# Django Libraries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
# Project Libraries
from hgfront.project.models import Project
from hgfront.wiki.models import WikiPage
from hgfront.wiki.forms import WikiPageCreateForm

def wiki_index(request, slug):
    """Return simple list of wiki pages"""
    try:
        page = WikiPage.objects.get(slug="Main_Page")
        project = Project.objects.get(name_short__exact=slug)
        return render_to_response('wiki/wiki_home.html', {'page':page, 'project':project})
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/edit/%s/" % "Main_Page/")

def wiki_page(request, slug, page_name):
    """Return a Wiki page"""
    try:
        page = WikiPage.objects.get(slug=page_name)
        return render_to_response('wiki/wiki_page.html', {'page':page})
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/edit/%s/" % page_name)
    
def wiki_edit(request, slug, page_name):
    """Create or edit and Wiki page"""
    if request.method == "POST":
        form = WikiPageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/%s/" % page_name)
    else:
        form = WikiPageCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('wiki/wiki_create.html', {'form':form, 'is_auth': is_auth, 'project':slug, 'page_name':page_name})
 
