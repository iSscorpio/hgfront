# General Libraries
# Django Libraries
from django.newforms import ModelForm
# Project Libraries
from hgfront.repo.models import Repo

class RepoCreateForm(ModelForm):
    """
    Create a repo
    """
    class Meta:
        model = Repo