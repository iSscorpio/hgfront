# General Libraries
# Django Libraries
from django.newforms import ModelForm
# Project Libraries
from hgfront.wiki.models import WikiPage

class WikiPageCreateForm(ModelForm):
    """
    Create a Wiki page
    """
    class Meta:
        model = WikiPage