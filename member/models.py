from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher

from project.models import Project

# Create your models here.

class Member(models.Model):
    user = models.ForeignKey(User, unique=True)
    member_displayname = models.CharField(max_length=25)
    member_homepage = models.URLField(blank = True, null = True)
    member_gtalk = models.CharField(max_length = 50, blank = True, null = True)
    member_msn = models.CharField(max_length = 50, blank = True, null = True)
    member_jabber = models.CharField(max_length = 50, blank = True, null = True)
    member_bio = models.TextField()
    
    def __unicode__(self):
        return self.user.username
    
    @permalink
    def get_absolute_url(self):
        """Creates a permalink to the project page"""
        return ('member-home', (), {})
    
    class Admin:
        list_display = ('user', 'member_displayname',)
        
class FavoriteProjects(models.Model):
    member = models.ForeignKey(Member)
    project = models.ForeignKey(Project)