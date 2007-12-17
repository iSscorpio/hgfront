from django.newforms import ModelForm
from hgfront.repo.models import Repo

class RepoCreateForm(ModelForm):
    """
    Create a repo
    """
    class Meta:
        model = Repo