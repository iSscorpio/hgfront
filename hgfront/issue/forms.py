# General Libraries
# Django Libraries
from django.newforms import ModelForm
# Project Libraries
from hgfront.issue.models import Issue

class IssueCreateForm(ModelForm):
    """
    Create a new issue!
    """
    class Meta:
        model = Issue
        exclude = ('project','user_posted','user_assigned_to','finished_date','pub_date')
