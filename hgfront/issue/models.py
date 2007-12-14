from django.db import models
from django.contrib.auth.models import User
from hgfront.project.models import Project
from mercurial import hg, ui
from django.conf import settings
from django.db.models import permalink
from django.core import urlresolvers
from django.dispatch import dispatcher
from django.db.models import signals
from hgfront.issue.signals import *

import datetime, sys, os, shutil

class IssueType(models.Model):
    """Represents the type of issue such as a bug or feature enhancment"""
    title=models.CharField(max_length=50)
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField()
    
    def __unicode__(self):
        return self.title
    
    def delete(self):
        self.is_active=0
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = 'issue type'
        verbose_name_plural = 'issue types'
        ordering = ['order']
#Dispatchers


class IssueSeverity(models.Model):
    """Represents how severe a issue is"""
    title=models.CharField(max_length=50)
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField()
    
    def __unicode__(self):
        return self.title
    
    def delete(self):
        self.is_active=0
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = 'issue severity'
        verbose_name_plural = 'issue severity'
        ordering = ['order']
#Dispatchers

        
class IssueStatus(models.Model):
    """Represents what stage a issue is at"""
    title=models.CharField(max_length=50)
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField()
    
    def __unicode__(self):
        return self.title
    
    def delete(self):
        self.is_active=0
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = 'issue status'
        verbose_name_plural = 'issue status'
        ordering = ['order']
#Dispatchers


class IssueManager(models.Manager):
    """A manager for issues"""
    def get_open_issues(self):
        return self.filter(date_finished__isnull=True)

    def get_closed_issues(self):
        return self.filter(date_finished__isnull=False)

class Issue(models.Model):
    """A class that represents an issue/bug"""
    objects = IssueManager()

    title = models.CharField(max_length=100)
    body = models.TextField()
    project = models.ForeignKey(Project)
    issue_type = models.ForeignKey(IssueType)
    issue_sev = models.ForeignKey(IssueSeverity)
    issue_status = models.ForeignKey(IssueStatus)
    user_posted = models.ForeignKey(User, related_name='user_posted', verbose_name='posted by')
    pub_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    user_assigned_to = models.ForeignKey(User, related_name='user_assigned_to', blank=True, null=True, verbose_name='assigned to')
    finished_date = models.DateTimeField(blank=True, null=True, verbose_name='finished on')

    def __unicode__(self):
        return self.title

    def completed(self):
        return self.finished_date is not None

    class Admin:
        list_display = ('title','project','pub_date','user_posted','user_assigned_to', 'issue_type', 'issue_sev', 'issue_status', 'completed')
        search_fields = ['title','body','foreign_key__related_user']
        list_filter = ['pub_date','project','user_posted', 'issue_type', 'issue_sev', 'issue_status']
        date_hierarchy = 'pub_date'

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['-pub_date']
#Dispatchers
dispatcher.connect( send_email_to_owner , signal=signals.post_save, sender=Issue )
