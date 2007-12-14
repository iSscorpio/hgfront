from django.newforms import ModelForm
from hgfront.project.models import Project, Repo

class ProjectCreateForm(ModelForm):
        class Meta:
            model = Project