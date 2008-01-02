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
    from hgfront.config.models import InstalledExtentions
    if InstalledExtentions in created_models:
        InstalledExtentions.objects.get_or_create(long_name='AclExtension', defaults={'short_name':'acl','long_name': 'AclExtension'})
        InstalledExtentions.objects.get_or_create(long_name='AliasExtension', defaults={'short_name':'alias','long_name': 'AliasExtension'})
        InstalledExtentions.objects.get_or_create(long_name='BisectExtension', defaults={'short_name':'bisect','long_name': 'BisectExtension'})
        InstalledExtentions.objects.get_or_create(long_name='BugzillaExtension', defaults={'short_name':'bugzilla','long_name': 'BugzillaExtension'})
        InstalledExtentions.objects.get_or_create(long_name='ChildrenExtension', defaults={'short_name':'children','long_name': 'ChildrenExtension'})
        InstalledExtentions.objects.get_or_create(long_name='ConvertExtension', defaults={'short_name':'convert','long_name': 'ConvertExtension'})
        InstalledExtentions.objects.get_or_create(long_name='ExtdiffExtension', defaults={'short_name':'extdiff','long_name': 'ExtdiffExtension'})
        InstalledExtentions.objects.get_or_create(long_name='FetchExtension', defaults={'short_name':'fetch','long_name': 'FetchExtension'})      
        InstalledExtentions.objects.get_or_create(long_name='GpgExtension', defaults={'short_name':'gpg','long_name': 'GpgExtension'})
        InstalledExtentions.objects.get_or_create(long_name='GraphlogExtension', defaults={'short_name':'graphlog','long_name': 'GraphlogExtension'})
        InstalledExtentions.objects.get_or_create(long_name='HgkExtension', defaults={'short_name':'hgk','long_name': 'HgkExtension'})
        InstalledExtentions.objects.get_or_create(long_name='ImergeExtension', defaults={'short_name':'imerge','long_name': 'ImergeExtension'})
        InstalledExtentions.objects.get_or_create(long_name='MqExtension', defaults={'short_name':'mq','long_name': 'MqExtension'})
        InstalledExtentions.objects.get_or_create(long_name='NotifyExtension', defaults={'short_name':'notify','long_name': 'NotifyExtension'})
        InstalledExtentions.objects.get_or_create(long_name='PatchbombExtension', defaults={'short_name':'patchbomb','long_name': 'PatchbombExtension'})
        InstalledExtentions.objects.get_or_create(long_name='RecordExtension', defaults={'short_name':'record','long_name': 'RecordExtension'})      
        InstalledExtentions.objects.get_or_create(long_name='TransplantExtension', defaults={'short_name':'transplant','long_name': 'TransplantExtension'})
        InstalledExtentions.objects.get_or_create(long_name='Win32Extension', defaults={'short_name':'win32text','long_name': 'Win32Extension'})        
        
        # Dispatchers       
dispatcher.connect(init_installed_styles, signal=signals.post_syncdb)
dispatcher.connect(init_installed_extentions, signal=signals.post_syncdb)