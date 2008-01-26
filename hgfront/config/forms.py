import django.newforms as forms
from hgfront.config.models import SiteOptions

class EditSiteOptions(ModelForm):
    """
    Edit site options.
    """
    class Meta:
        model = SiteOptions
