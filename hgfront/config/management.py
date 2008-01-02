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
        
# Dispatchers       
dispatcher.connect(init_installed_styles, signal=signals.post_syncdb)