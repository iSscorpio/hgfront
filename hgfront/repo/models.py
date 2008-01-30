# General Libraries
import datetime, sys, os, shutil
from mercurial.cmdutil import revrange, show_changeset
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
import hgfront.config
from hgfront.repo import signals as hgsignals
from hgfront.repo.signals import *
from hgfront.project.models import Project

REPO_TYPES = (
    (1, 'New',),
    (2, 'Clone',),
)

available_styles = (
    ('default', 'Default'),
    ('gitweb', 'Gitweb'),
)

class Repo(models.Model):
    """A repo represents a physical repository on the hg system path"""
    creation_method=models.IntegerField(max_length=1, choices=REPO_TYPES, verbose_name="Is this new or cloned?")
    name_short=models.CharField(max_length=20)
    name_long=models.CharField(max_length=50)
    description_short=models.CharField(max_length=255, null=True, blank=True)
    default_path=models.CharField(max_length=255, null=True, blank=True)
    repo_contact=models.ForeignKey(User, related_name="repo_contact")
    parent_project=models.ForeignKey(Project)
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    anonymous_pull=models.BooleanField(default=True)
    anonymous_push=models.BooleanField(default=False)
    pull_members=models.ManyToManyField(User, related_name="pull_members", null=True, blank=True)
    push_members=models.ManyToManyField(User, related_name="push_members", null=True, blank=True)
    hgweb_style=models.CharField(max_length=50,choices=available_styles)
    
    offer_zip=models.BooleanField(default=True)
    offer_tar=models.BooleanField(default=True)
    offer_bz2=models.BooleanField(default=True)
    
    #active_extensions=models.ManyToManyField(InstalledExtensions)

    def __unicode__(self):
        return self.name_long
        
    def get_absolute_url(self):
        """Get the URL of this entry to create a permalink"""
        return ('view-tip', (), {
            "slug": self.parent_project.name_short,
            "repo_name": self.name_short
            })
    get_absolute_url = permalink(get_absolute_url)
    
    def was_cloned(self):
        """Checks to see if this was a cloned repositories"""
        return bool(self.creation_method == '2')
    was_cloned.short_description = "Cloned Repository?"
    
    def repo_directory(self):
        return os.path.join(Project.project_options.repository_directory, self.parent_project.name_short, self.name_short)
    
    def get_branches(self):
        u = ui.ui()  # get a ui object
        r = hg.repository(u, self.repo_directory())
        b = r.branchtags() # get a repo object for the current directory
        branches = b.keys()
        branches.sort()
        return branches            
    
    def get_changeset_number(self):
        u = ui.ui()
        r = hg.repository(u, self.repo_directory())
        c = r.changectx('tip').rev()
        print c
        return c
        
    def get_changeset(self, changeset="tip"):
        u = ui.ui()  # get a ui object
        r = hg.repository(u, self.repo_directory()) # get a repo object for the current directory
        c = r.changectx(changeset) # get a context object for the "tip" revision
        return c
        
    def get_tags(self):
        u = ui.ui()  # get a ui object
        r = hg.repository(u, self.repo_directory()) # get a repo object for the current directory
        return r.tags()
        
    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('creation_method', 'name_short', 'name_long', 'default_path', 'description_short', 'parent_project', )}),
                  ('Repository Access', {'fields': ('anonymous_pull', 'pull_members', 'anonymous_push', 'push_members', 'repo_contact')}),
                  ('Archive Information', {'fields': ('offer_zip', 'offer_tar', 'offer_bz2', 'hgweb_style')}),
                  #('Active Extentions', {'fields': ('active_extensions',)}),
                  ('Date information', {'fields': ('pub_date',)}),
        )
        list_display = ('name_long', 'parent_project', 'was_cloned', 'pub_date',)
        list_filter = ['pub_date', 'parent_project',]
        search_fields = ['name_long', 'parent_project']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)

    class Meta:
        unique_together=('parent_project','name_short')


# Dispatchers
dispatcher.connect( create_repo , signal=signals.post_save, sender=Repo )
dispatcher.connect( delete_repo , signal=signals.post_delete, sender=Repo )
