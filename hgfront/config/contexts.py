from django.template import Context

def sitename(request):
    from hgfront.config.models import SiteOptions
    sitename = SiteOptions.objects.get(option_key__exact = 'sitename')
    return {'sitename': sitename.option_value}
