# General Libraries

# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher

# Project Libraries

class InstalledStyles(models.Model):
    """This stores a list of installed hgweb styles"""
    short_name=models.CharField(max_length=50, db_index=True)
    long_name=models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.long_name
    
    class Admin:
        pass
    
class InstalledExtentions(models.Model):
    """This stores a list of installed hg extentions"""
    short_name=models.CharField(max_length=50, db_index=True)
    long_name=models.CharField(max_length=100)
    
    class Admin:
        pass