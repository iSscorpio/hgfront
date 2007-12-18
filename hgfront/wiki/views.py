# General Libraries
# Django Libraries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
# Project Libraries
from hgfront.project.models import Project
from hgfront.wiki.models import WikiPage
from hgfront.wiki.forms import WikiPageCreateForm

def wiki_index(request, slug):
    """Return simple list of wiki pages"""
    pages = WikiPage.objects.all().filter(project__name_short=slug).order_by('title')
    project = Project.objects.get(name_short__exact=slug)
    return render_to_response('wiki/wiki_home.html', {'pages':pages, 'project':project})

def wiki_page(request, slug, page_name):
    """Return a Wiki page"""
    try:
        page = WikiPage.objects.get(slug=page_name)
        project = page.project
        return render_to_response('wiki/wiki_page.html', {'page':page, 'project':project})
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect(reverse('wiki-edit', kwargs={'slug':project.name_short,'page_name':page_name}))
    
def wiki_edit(request, slug, page_name):
    """Create or edit and Wiki page"""
    project = Project.objects.get(name_short=slug)
    if request.method == "POST":
        form = WikiPageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wiki-page', kwargs={'slug':project.name_short,'page_name':page_name}))
    else:
        form = WikiPageCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('wiki/wiki_create.html', {'form':form, 'is_auth': is_auth, 'project':project, 'page_name':page_name})
 
