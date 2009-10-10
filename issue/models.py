# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify
# Project Libraries
from core.configs import IssueOptions
from issue.signals import *
from project.models import Project
from repo.models import Repo

class IssueType(models.Model):
    """Represents the type of issue such as a bug or feature enhancment"""
    title=models.CharField(max_length=50)
    slug=models.SlugField()
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField(default=1)
    force_insert=False;

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(IssueType, self).save()

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
    slug=models.SlugField()
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField(default=1)

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(IssueSeverity, self).save()

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
    slug=models.SlugField()
    order=models.IntegerField(max_length=3)
    is_active=models.BooleanField(default=1)

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(IssueStatus, self).save()

    def delete(self):
        self.is_active=0

    class Admin:
        pass

    class Meta:
        verbose_name = 'issue status'
        verbose_name_plural = 'issue status'
        ordering = ['order']
#Dispatchers

class IssueQuerySet(models.query.QuerySet):
    """
    Overiding the Issue default queryset for Issues as per http://www.djangosnippets.org/snippets/562/
    """
    def get_open_issues(self):
        return self.filter(finished_date__isnull=True)

    def get_closed_issues(self):
        return self.filter(finished_date__isnull=False)

class IssueManager(models.Manager):
    """
    A manager for issues.  Since we're overiding the queryset, we can chain the functions
    as per http://www.djangosnippets.org/snippets/562/
    """
    def get_query_set(self):
        model = models.get_model('issue', 'Issue')
        return IssueQuerySet(model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

class Issue(models.Model):
    """A class that represents an issue/bug"""
    objects = IssueManager()

    title = models.CharField(max_length=100)
    body = models.TextField()
    project = models.ForeignKey(Project)
    issue_type = models.ForeignKey(IssueType)
    issue_sev = models.ForeignKey(IssueSeverity)
    issue_status = models.ForeignKey(IssueStatus)
    issue_repos = models.ManyToManyField(Repo, blank=True, null=True)
    user_posted = models.ForeignKey(User, blank=True, null=True, related_name='posted_issues', verbose_name='posted by')
    user_assigned_to = models.ForeignKey(User, related_name='assigned_issues', blank=True, null=True, verbose_name='assigned to')
    # created_date: The date the issue instance was created
    created_date=models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created on')
    # modified_date: The date the issue instance was last modified
    modified_date=models.DateTimeField(auto_now=True, editable=False, verbose_name='last updated')
    # finished_date: The date the issue instance was closed
    finished_date = models.DateTimeField(blank=True, null=True, verbose_name='finished on')


    @permalink
    def get_absolute_url(self):
        return ('issue-detail',(),{'slug':self.project.project_id,'issue_id':self.pk})
    def __unicode__(self):
        return self.title

    def completed(self):
        return self.finished_date is not None
        
    issue_options = IssueOptions()

    class Admin:
        list_display = ('title','project','created_date','user_posted','user_assigned_to', 'issue_type', 'issue_sev', 'issue_status', 'completed')
        search_fields = ['title','body','foreign_key__related_user']
        list_filter = ['created_date','project','user_posted', 'issue_type', 'issue_sev', 'issue_status']
        date_hierarchy = 'created_date'

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['-created_date']
#Dispatchers
signals.post_save.connect( send_email_to_owner , sender=Issue )
