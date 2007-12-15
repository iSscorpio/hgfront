from django.newforms import ModelForm
from hgfront.wiki.models import WikiPage

class WikiPageCreateForm(ModelForm):
    """
    Create a Wiki page
    """
    class Meta:
        model = WikiPage