from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from hgfront.wiki.models import WikiPage
from hgfront.project.models import Project
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
        return render_to_response('wiki/wiki_page.html', {'page':page})
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/edit/%s/" % page_name)
    
def wiki_edit(request, slug, page_name):
    if request.method == "POST":
        form = WikiPageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/%s/" % page_name)
    else:
        form = WikiPageCreateForm()
    is_auth = bool(request.user.is_authenticated())
    return render_to_response('wiki/wiki_create.html', {'form':form, 'is_auth': is_auth, 'project':slug, 'page_name':page_name})
 
