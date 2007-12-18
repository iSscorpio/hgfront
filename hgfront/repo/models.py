# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
from hgfront.repo.signals import *
from hgfront.project.models import Project

REPO_TYPES = (
    ('1', 'New',),
    ('2', 'Clone',),
)

class Repo(models.Model):
    """A repo represents a physical repository on the hg system path"""
    creation_method=models.IntegerField(max_length=1, choices=REPO_TYPES, verbose_name="Is this new or cloned?")
    repo_name=models.CharField(max_length=20)
    repo_dirname=models.CharField(max_length=20)
    repo_description=models.CharField(max_length=255, null=True, blank=True)
    repo_url=models.URLField(null=True, blank=True)
    project=models.ForeignKey(Project)
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    anonymous_pull=models.BooleanField(default=True)
    
    offer_zip=models.BooleanField(default=True)
    offer_tar=models.BooleanField(default=True)
    offer_bz2=models.BooleanField(default=True)

    def __unicode__(self):
        return self.repo_name

    def get_absolute_url(self):
        """Get the URL of this entry to create a permalink"""
        return ('repo-detail', (), {
            "slug": self.project.name_short,
            "repo_name": self.repo_name
            })
    get_absolute_url = permalink(get_absolute_url)

    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('creation_method', 'repo_name', 'repo_dirname', 'repo_url', 'repo_description', 'project', 'anonymous_pull')}),
                  ('Archive Information', {'fields': ('offer_zip', 'offer_tar', 'offer_bz2',)}),
                  ('Date information', {'fields': ('pub_date',)}),
        )
        list_display = ('repo_name', 'project', 'pub_date',)
        list_filter = ['pub_date', 'project',]
        search_fields = ['name_long', 'project']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)

    class Meta:
        unique_together=('project','repo_name')


# Dispatchers
dispatcher.connect( create_repo , signal=signals.post_save, sender=Repo )
dispatcher.connect( delete_repo , signal=signals.post_delete, sender=Repo )
