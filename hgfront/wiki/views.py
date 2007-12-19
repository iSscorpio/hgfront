# General Libraries
# Django Libraries
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
# Project Libraries
from hgfront.project.models import Project
from hgfront.wiki.models import WikiPage
from hgfront.wiki.forms import WikiPageCreateForm
from hgfront.project.decorators import check_project_permission

@check_project_permission('view_wiki')
def wiki_page(request, slug, page_name):
    """Return a Wiki page"""
    try:
        page = WikiPage.objects.get(slug=page_name)
        project = Project.objects.get(name_short__exact=slug)
        return render_to_response('wiki/wiki_page.html',
                {
                     'page':page,
                     'project':project,
                     'permissions': project.get_permissions(request.user),
                }
        )
    except WikiPage.DoesNotExist:
        # FIXME: This does not redirect properly
        return HttpResponseRedirect(reverse('wiki-edit', kwargs={'slug':slug, 'page_name':page_name}))

@check_project_permission('edit_wiki')    
def wiki_edit(request, slug, page_name):
    """Create or edit and Wiki page"""
    if request.method == "POST":
        form = WikiPageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/hgfront/projects/" + slug + "/wiki/%s/" % page_name)
    else:
        form = WikiPageCreateForm()
    return render_to_response('wiki/wiki_create.html',
                {
                     'form':form,
                     'project':slug,
                     'page_name':page_name,
                     'permissions': project.get_permissions(request.user),
                 }
    )
 
