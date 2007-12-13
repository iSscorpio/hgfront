from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from mercurial import hg, ui
from django.conf import settings
from django.db.models import permalink
from django.core import urlresolvers
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
    private=models.BooleanField(default=False)
    user=models.ForeignKey(User)
    group=models.ManyToManyField(Group)
    pub_date=models.DateTimeField('date published')
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
                  ('Project Creation', {'fields': ('longname', 'shortname', 'description', 'group', )}),
                  ('Date information', {'fields': ('pub_date',)}),
                  ('Publishing Details', {'fields': ('user', 'private',)}),
        )
        list_display = ('longname', 'shortname', 'num_repos', 'private', 'user', 'pub_date',)
        list_filter = ['pub_date', 'private']
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
    def __unicode__(self):
        return self.name
    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('creation_method', 'name', 'url', 'project',)}),
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
