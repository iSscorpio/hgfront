from django.template import Context
from hgfront.config.models import SiteOptions
def site_options(request):
    return dict([(option.option_key, option.option_value) for option in SiteOptions.objects.all()])
