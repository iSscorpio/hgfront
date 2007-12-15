from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import permalink
from django.dispatch import dispatcher
from django.db.models import signals
from hgfront.repo.signals import *
from hgfront.project.models import Project

import datetime, sys, os, shutil

REPO_TYPES = (
    ('1', 'New',),
    ('2', 'Clone',),
)

class Repo(models.Model):
    """A repo represents a physical repository on the hg system path"""
    creation_method=models.IntegerField(max_length=1, choices=REPO_TYPES, verbose_name="Repository")
    name=models.CharField(max_length=20, db_index=True)
    url=models.URLField(null=True, blank=True)
    project=models.ForeignKey(Project)
    pub_date=models.DateTimeField('date published')
    anonymous=models.BooleanField(default=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        """Get the URL of this entry to create a permalink"""
        return ('repo-detail', (), {
            "slug": self.project.shortname,
            "repo_name": self.name
            })
    get_absolute_url = permalink(get_absolute_url)
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
dispatcher.connect( create_repo , signal=signals.post_save, sender=Repo )
dispatcher.connect( delete_repo , signal=signals.post_delete, sender=Repo )
