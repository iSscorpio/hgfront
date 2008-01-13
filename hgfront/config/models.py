# General Libraries

# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher

# Project Libraries

class SiteOptions(models.Model):
    """This is the general options model"""
    option_key=models.CharField(max_length=50, db_index=True)
    option_keydesc=models.CharField(max_length=100)
    option_value=models.TextField()
    option_description=models.TextField()
    option_active=models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.option_keydesc

    def get_option(self, key):
        """This returns a specific option by key"""
        return SiteOptions.objects.get(option_key__extact = key)

    class Admin:
        pass
        
    class Meta:
        verbose_name = 'hgfront option'
        verbose_name_plural = 'hgfront options'
        ordering = ['option_key']
        

class InstalledStyles(models.Model):
    """This stores a list of installed hgweb styles"""
    short_name=models.CharField(max_length=50, db_index=True)
    long_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.long_name
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = 'installed style'
        verbose_name_plural = 'installed styles'
        ordering = ['short_name']
    
class InstalledExtensions(models.Model):
    """This stores a list of installed hg extentions"""
    short_name=models.CharField(max_length=50, db_index=True)
    long_name=models.CharField(max_length=100)
    additional_options=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.long_name
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = 'installed extention'
        verbose_name_plural = 'installed extentions'
        ordering = ['short_name']
