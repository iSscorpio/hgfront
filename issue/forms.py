# General Libraries
# Django Libraries
from django.forms import ModelForm
from django import forms
# Project Libraries
from issue.models import Issue

class IssueCreateForm(ModelForm):
    """
    Create a new issue!
    """
    class Meta:
        model = Issue
        exclude = ('project','issue_status','user_posted','user_assigned_to', 'created_date', 'modified_date', 'finished_date',)

class IssueEditForm(ModelForm):
    """
    Edit an issue!
    """
    class Meta:
        model = Issue
        exclude = ('title','body','project','user_posted', 'created_date',)
