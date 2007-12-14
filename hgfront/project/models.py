from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.db.models import permalink
from django.dispatch import dispatcher
from django.db.models import signals
from hgfront.project.signals import *

import datetime, sys, os, shutil

# Create your models here.
class Project(models.Model):
    """A project is a way to group users and repositories"""
    longname=models.CharField(max_length=255)
    shortname=models.CharField(max_length=50)
    description=models.TextField()
    is_private=models.BooleanField(default=False)
    user_owner=models.ForeignKey(User, related_name='user_owner', verbose_name='project owner')
    user_members=models.ManyToManyField(User, related_name='user_members', verbose_name='project members', null=True, blank=True)
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    def __unicode__(self):
        return self.longname
    def num_repos(self):
        """Returns the number of repositories in this project"""
        return self.repo_set.count()
    num_repos.short_description = "Number of Repositories"
    def get_absolute_url(self):
        """Get the URL of this entry to create a permalink"""
        return ('project-detail', (), {
            "slug": self.shortname
            })
    get_absolute_url = permalink(get_absolute_url)
    class Admin:
        fields = (
                  ('Project Creation', {'fields': ('longname', 'shortname', 'description',)}),
                  ('Date information', {'fields': ('pub_date',)}),
                  ('Publishing Details', {'fields': ('user_owner', 'user_members', 'is_private',)}),
        )
        list_display = ('longname', 'shortname', 'num_repos', 'is_private', 'user_owner', 'pub_date',)
        list_filter = ['pub_date', 'is_private']
        search_fields = ['longname', 'description']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)
# Dispatchers
dispatcher.connect( create_project_dir , signal=signals.pre_save, sender=Project )
dispatcher.connect( delete_project_dir , signal=signals.post_delete, sender=Project )

REPO_TYPES = (
    ('1', 'New',),
    ('2', 'Clone',),
)

class Repo(models.Model):
    """A repo represents a physical repository on the hg system path"""
    creation_method=models.IntegerField(max_length=1, choices=REPO_TYPES, verbose_name="Repository")
    name=models.CharField(max_length=20, null=True, blank=True)
    url=models.URLField(null=True, blank=True)
    project=models.ForeignKey(Project)
    pub_date=models.DateTimeField('date published')
    anonymous=models.BooleanField(default=True)
    def __unicode__(self):
        return self.name
    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('creation_method', 'name', 'url', 'project', 'anonymous')}),
                  ('Date information', {'fields': ('pub_date',)}),
        )
        list_display = ('name', 'project', 'pub_date',)
        list_filter = ['pub_date', 'project',]
        search_fields = ['longname', 'project']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)
# Dispatchers
dispatcher.connect( create_repo , signal=signals.pre_save, sender=Repo )
dispatcher.connect( delete_repo , signal=signals.post_delete, sender=Repo )

class ProjectPermissionSet(models.Model):
    """A set of permissions for a user in a given project"""
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    push = models.BooleanField(default=True)
    pull = models.BooleanField(default=False)

    add_repos = models.BooleanField(default=False)
    delete_repos = models.BooleanField(default=False)
    edit_repos = models.BooleanField(default=False)
    view_repos = models.BooleanField(default=True)

    add_issues = models.BooleanField(default=False)
    delete_issues = models.BooleanField(default=False)
    edit_issues = models.BooleanField(default=False)
    view_issues = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "Permissions for %s in %s" % (self.user.username, self.project.shortname)

    class Admin:
        pass
