# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
# Project Libraries
from hgfront.project.models import Project
from hgfront.repo.models import Repo

class RepoCreateForm(forms.ModelForm):
    """
    Create a repo
    """
    
    class Meta:
        model = Repo
        exclude = ('created', 'local_parent_project','local_creation_date','local_manager')