# General Libraries
# Django Libraries
from django.newforms import ModelForm
import django.newforms as forms
# Project Libraries
from hgfront.issue.models import Issue

class IssueCreateForm(ModelForm):
    """
    Create a new issue!
    """
    class Meta:
        model = Issue
        exclude = ('project','user_posted','finished_date','pub_date')

class IssueEditForm(ModelForm):
    """
    Edit an issue!
    """
    class Meta:
        model = Issue
        exclude = ('project','user_posted','finished_date','pub_date')
