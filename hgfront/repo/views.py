from django.http import HttpResponse

def repo_list(request, slug):
   return HttpResponse("repo list") 

def repo_detail(request, repo_id, slug=None):
   return HttpResponse("repo detail") 
