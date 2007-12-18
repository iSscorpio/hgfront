# General Libraries
# Django Libraries
from django.newforms import ModelForm
# Project Libraries
from hgfront.project.models import Project

class ProjectCreateForm(ModelForm):
    """
    This form allows a registered user to create a project in the system.
    When a project is created, it also creates a directory to store the data in.
    """
    class Meta:
        model = Project