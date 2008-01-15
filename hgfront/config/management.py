"""
Creates default values for the configs
"""
# General Libraries
# Django Libraries
from django.conf import settings
from django.db.models import get_models, signals
from django.dispatch import dispatcher
# Project Libraries

def init_installed_styles(app, created_models, verbosity, **kwargs):
    """Default styles installed"""
    from hgfront.config.models import InstalledStyles
    if InstalledStyles in created_models:
        InstalledStyles.objects.get_or_create(long_name='Default', defaults={'short_name':'default','long_name': 'Default'})
        InstalledStyles.objects.get_or_create(long_name='Gitweb', defaults={'short_name':'gitweb','long_name': 'Gitweb'})

def init_installed_extentions(app, created_models, verbosity, **kwargs):
    """Default styles installed"""
    from hgfront.config.models import InstalledExtensions
    if InstalledExtensions in created_models:
        InstalledExtensions.objects.get_or_create(long_name='AclExtension', defaults={'short_name':'acl','long_name': 'AclExtension'})
        InstalledExtensions.objects.get_or_create(long_name='AliasExtension', defaults={'short_name':'alias','long_name': 'AliasExtension'})
        InstalledExtensions.objects.get_or_create(long_name='BisectExtension', defaults={'short_name':'bisect','long_name': 'BisectExtension'})
        InstalledExtensions.objects.get_or_create(long_name='BugzillaExtension', defaults={'short_name':'bugzilla','long_name': 'BugzillaExtension'})
        InstalledExtensions.objects.get_or_create(long_name='ChildrenExtension', defaults={'short_name':'children','long_name': 'ChildrenExtension'})
        InstalledExtensions.objects.get_or_create(long_name='ConvertExtension', defaults={'short_name':'convert','long_name': 'ConvertExtension'})
        InstalledExtensions.objects.get_or_create(long_name='ExtdiffExtension', defaults={'short_name':'extdiff','long_name': 'ExtdiffExtension'})
        InstalledExtensions.objects.get_or_create(long_name='FetchExtension', defaults={'short_name':'fetch','long_name': 'FetchExtension'})      
        InstalledExtensions.objects.get_or_create(long_name='GpgExtension', defaults={'short_name':'gpg','long_name': 'GpgExtension'})
        InstalledExtensions.objects.get_or_create(long_name='GraphlogExtension', defaults={'short_name':'graphlog','long_name': 'GraphlogExtension'})
        InstalledExtensions.objects.get_or_create(long_name='HgkExtension', defaults={'short_name':'hgk','long_name': 'HgkExtension'})
        InstalledExtensions.objects.get_or_create(long_name='ImergeExtension', defaults={'short_name':'imerge','long_name': 'ImergeExtension'})
        InstalledExtensions.objects.get_or_create(long_name='MqExtension', defaults={'short_name':'mq','long_name': 'MqExtension'})
        InstalledExtensions.objects.get_or_create(long_name='NotifyExtension', defaults={'short_name':'notify','long_name': 'NotifyExtension'})
        InstalledExtensions.objects.get_or_create(long_name='PatchbombExtension', defaults={'short_name':'patchbomb','long_name': 'PatchbombExtension'})
        InstalledExtensions.objects.get_or_create(long_name='RecordExtension', defaults={'short_name':'record','long_name': 'RecordExtension'})      
        InstalledExtensions.objects.get_or_create(long_name='TransplantExtension', defaults={'short_name':'transplant','long_name': 'TransplantExtension'})
        InstalledExtensions.objects.get_or_create(long_name='Win32Extension', defaults={'short_name':'win32text','long_name': 'Win32Extension'})        

def init_default_options(app, created_models, verbosity, **kwargs):
    """Default Options"""
    from hgfront.config.models import SiteOptions
    if SiteOptions in created_models:
        SiteOptions.objects.get_or_create(option_key='hgf_site_name', defaults={'option_key':'hgf_site_name', 'option_keydesc':'Site Name','option_value':'hgfront Dev Application', 'option_description':'The site name', 'option_active':'1'})
        SiteOptions.objects.get_or_create(option_key='hgf_site_url', defaults={'option_key':'hgf_site_url', 'option_keydesc':'Site URL','option_value':'http://127.0.0.1:8000/hgfront/', 'option_description':'The URL of the site', 'option_active':'1'})        
        SiteOptions.objects.get_or_create(option_key='hgf_site_admin_url', defaults={'option_key':'hgf_site_admin_url', 'option_keydesc':'Site Admin URL','option_value':'http://127.0.0.1:8000/admin/', 'option_description':'The URL of the sites admin', 'option_active':'1'})
        SiteOptions.objects.get_or_create(option_key='hgf_site_owner', defaults={'option_key':'hgf_site_owner', 'option_keydesc':'Site Owner','option_value':'Default Owner', 'option_description':'The name of the site owner', 'option_active':'1'})
        SiteOptions.objects.get_or_create(option_key='hgf_site_owner_email', defaults={'option_key':'hgf_site_owner_email', 'option_keydesc':'Site Admin URL','option_value':'http://127.0.0.1:8000/admin/', 'option_description':'The URL of the sites admin', 'option_active':'1'})
        SiteOptions.objects.get_or_create(option_key='hgf_repo_location', defaults={'option_key':'hgf_repo_location', 'option_keydesc':'Repo Location','option_value':'/path/to/repos/', 'option_description':'The location of your repos', 'option_active':'1'})        
                
# Dispatchers       
dispatcher.connect(init_installed_styles, signal=signals.post_syncdb)
dispatcher.connect(init_installed_extentions, signal=signals.post_syncdb)
dispatcher.connect(init_default_options, signal=signals.post_syncdb)
