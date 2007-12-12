from django.db import models
from django.contrib.auth.models import User
from hgfront.project.models import Project
from mercurial import hg, ui
from django.conf import settings
from django.db.models import permalink
from django.core import urlresolvers

import datetime, sys, os, shutil

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
    user_posted = models.ForeignKey(User, related_name='user_posted', verbose_name='posted by')
    pub_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    user_assigned_to = models.ForeignKey(User, related_name='user_assigned_to', blank=True, null=True, verbose_name='assigned to')
    finished_date = models.DateTimeField(blank=True, null=True, verbose_name='finished on')

    def __unicode__(self):
        return self.title

    def completed(self):
        return self.finished_date is not None

    class Admin:
        list_display = ('title','project','pub_date','user_posted','user_assigned_to','completed')
        search_fields = ['title','body','foreign_key__related_user']
        list_filter = ['pub_date','project','user_posted']
        date_hierarchy = 'pub_date'

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['-pub_date']

