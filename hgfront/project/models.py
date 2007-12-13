from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from mercurial import hg, ui
from django.conf import settings
from django.db.models import permalink
from django.core import urlresolvers

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
    def save(self):
        """Create the project path on the system and then save the model"""
        return bool(shutil.os.mkdir(settings.MERCURIAL_REPOS + self.shortname))
        super(Project, self).save()
    def delete(self):
        """Delete the model and then remove the path"""
        super(Project, self).delete()
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + self.shortname))
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
    def save(self):
        """Call for the creation of a repo first before saving model"""
        if self.creation_method=='1':
            self.create_repo()
        elif self.creation_method=='2':
            self.clone_repo()
        else:
            raise ValueError("Invalid value: %r" % self.creation_method)
        super(Repo, self).save()
    def delete(self):
        """Delete the repo first before the model"""
        super(Repo, self).delete()
        self.remove_repo()
    def create_repo(self):
        """Create the mercurial repo"""
        p = Project.objects.get(longname=self.project)
        u = ui.ui()
        return bool(hg.repository(u, str(settings.MERCURIAL_REPOS + p.shortname + '/' + self.name), create=True))
    def clone_repo(self):
        """Clone a repo via http"""
        p = Project.objects.get(longname=self.project)
        u = ui.ui()
        return bool(hg.clone(u, str(self.url), str(settings.MERCURIAL_REPOS + p.shortname + '/' + self.name), True))
    def remove_repo(self):
        """Destroy the mercurial repo"""
        p = Project.objects.get(longname=self.project)
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + p.shortname + '/' + self.name))
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
