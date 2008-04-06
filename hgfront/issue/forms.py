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
        exclude = ('project','issue_status','user_posted','user_assigned_to', 'created_date', 'modified_date', 'finished_date',)

class IssueEditForm(ModelForm):
    """
    Edit an issue!
    """
    class Meta:
        model = Issue
        exclude = ('title','body','project','user_posted', 'created_date',)
