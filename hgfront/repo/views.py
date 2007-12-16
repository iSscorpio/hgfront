from django.http import HttpResponse

def repo_list(request, slug):
   return HttpResponse("repo list") 

def repo_detail(request, slug, repo_name):
   return HttpResponse("repo detail") 

def repo_create(request, slug):
    return HttpResponse("repo create")