from django.template import Context

def hgf_site_name(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_site_name')
    return {'hgf_site_name': option.option_value}
    
def hgf_site_url(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_site_url')
    return {'hgf_site_url': option.option_value}
    
def hgf_site_admin_url(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_site_admin_url')
    return {'hgf_site_admin_url': option.option_value}
    
def hgf_site_owner(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_site_owner')
    return {'hgf_site_owner': option.option_value}

def hgf_site_owner_email(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_site_owner_email')
    return {'hgf_site_owner_email': option.option_value}
    
def hgf_repo_location(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_repo_location')
    return {'hgf_repo_location': option.option_value}
    
def hgf_issues_per_page(request):
    from hgfront.config.models import SiteOptions
    option = SiteOptions.objects.get(option_key = 'hgf_issues_per_page')
    return {'hgf_issues_per_page': option.option_value}
