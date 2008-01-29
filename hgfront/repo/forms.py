# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.models import Repo

#class RepoCreateForm(forms.Form):
#    repo_dirname = forms.CharField(max_length=50)
    
#class RepoCreateStep2(forms.Form):
#    repo_dirname = forms.CharField(max_length=50)
#    repo_name = forms.CharField(max_length=100)
#    repo_description = forms.CharField(widget=forms.widgets.Textarea())
#    creation_method = MultipleChoiceField([(1,'New'),(2, 'Cloned')])
#    repo_url = forms.CharField(max_length=255)  # There is probably a URL field for this
#    repo_contact = forms.CharField()
#    project = forms.CharField()
#    pub_date = forms.DateTimeField()
#    anonymous_pull = forms.BooleanField()
#    anonymous_push = forms.BooleanField()
#    # To build the rest


class RepoCreateForm(forms.ModelForm):
    """
    Create a repo
    """
    class Meta:
        model = Repo
        exclude = ('project','pub_date')
        
#class CloneRepoForm(forms.Form):
#    name_short = forms.CharField(max_length=50)
