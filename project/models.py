from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from mercurial import hg, ui
from django.conf import settings

import datetime, sys, os, shutil

# Create your models here.
class Project(models.Model):
    """A project is a way to group users and repositories"""
    longname=models.CharField(max_length=255)
    shortname=models.CharField(max_length=50)
    description=models.TextField()
    private=models.BooleanField(default=False)
    user=models.ForeignKey(User)
    pub_date=models.DateTimeField('date published')
    def __unicode__(self):
        return self.longname
    def num_repos(self):
        """Returns the number of repositories in this project"""
        return self.repo_set.count()
    num_repos.short_description = "Number of Repositories"
    class Admin:
        fields = (
                  ('Project Creation', {'fields': ('longname', 'shortname', 'description',)}),
                  ('Date information', {'fields': ('pub_date',)}),
                  ('Publishing Details', {'fields': ('user', 'private',)}),
        )
        list_display = ('longname', 'shortname', 'num_repos', 'private', 'user', 'pub_date',)
        list_filter = ['pub_date', 'private']
        search_fields = ['longname', 'description']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)
    
class Repo(models.Model):
    """A repo represents a physical repository on the hg system path"""
    name=models.CharField(max_length=20)
    project=models.ForeignKey(Project)
    pub_date=models.DateTimeField('date published')
    def __unicode__(self):
        return self.name
    def save(self):
        """Call for the creation of a repo first before saving model"""
        self.create_repo()
        super(Repo, self).save()
    def delete(self):
        """Delete the repo first before the model"""
        self.remove_repo()
        super(Repo, self).delete()
    def create_repo(self):
        """Create the mercurial repo"""
        u = ui.ui()
        return bool(hg.repository(u, settings.MERCURIAL_REPOS + self.name, create=True))
    def remove_repo(self):
        """Destroy the mercurial repo"""
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + self.name))
    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('name', 'project',)}),
                  ('Date information', {'fields': ('pub_date',)}),
        )
        list_display = ('name', 'project', 'pub_date',)
        list_filter = ['pub_date', 'project',]
        search_fields = ['longname', 'project']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)