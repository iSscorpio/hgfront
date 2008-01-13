from django.template import Context

def sitename(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'sitename')
    return {'sitename': option.option_value}
    
def siteurl(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'siteurl')
    return {'siteurl': option.option_value}
    
def siteadminurl(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'siteadminurl')
    return {'siteadminurl': option.option_value}
