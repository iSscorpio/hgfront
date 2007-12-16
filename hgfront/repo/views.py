from django.http import HttpResponse

def repo_list(request, slug):
   return HttpResponse("repo list") 

def repo_detail(request, repo_name, slug):
   return HttpResponse("repo detail") 
