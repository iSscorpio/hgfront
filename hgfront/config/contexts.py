from django.template import Context
from hgfront.config.models import SiteOptions
def site_options(request):
    """
    This function returns the all the site options as a dictionary and prefixes the keys with hgf_
    So if there's a site option with the key site_name, to access it just use {{hgf_site_name}}
    """
    return dict([('hgf_'+option.option_key, option.option_value) for option in SiteOptions.objects.all()])
