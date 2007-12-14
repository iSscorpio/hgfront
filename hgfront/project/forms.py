from django.newforms import ModelForm
from hgfront.project.models import Project, Repo

class ProjectCreateForm(ModelForm):
    """Creates a project creation form from the Project model"""
    class Meta:
        model = Project