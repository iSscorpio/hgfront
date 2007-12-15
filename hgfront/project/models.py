from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import permalink
from django.dispatch import dispatcher
from django.db.models import signals
from hgfront.project.signals import *

import datetime, sys, os, shutil

# Create your models here.
class Project(models.Model):
    """
    A project represents a way to group users, repositories and issues on the system.
    Each project has a project owner who has full control over all aspects of the project.  When
    a project is created, it is also given a default set of permissions for non-members, which are
    changeable
    
    You can also assign members to a project, and give them each their own permission set.
    """
    longname=models.CharField(max_length=255)
    shortname=models.CharField(max_length=50, unique=True, db_index=True)
    description=models.TextField()
    is_private=models.BooleanField(default=False)
    user_owner=models.ForeignKey(User, related_name='user_owner', verbose_name='project owner')
    user_members=models.ManyToManyField(User, related_name='user_members', verbose_name='project members', null=True, blank=True)
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    def __unicode__(self):
        return self.longname
    def num_repos(self):
        """Returns the number of repositories linked to this project"""
        return self.repo_set.count()
    num_repos.short_description = "Number of Repositories"
    def get_absolute_url(self):
        """Creates a permalink to the project page"""
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
dispatcher.connect( create_default_permission_set, signal=signals.post_save, sender=Project )
dispatcher.connect( create_project_dir , signal=signals.post_save, sender=Project )
dispatcher.connect( delete_project_dir , signal=signals.post_delete, sender=Project )

#TODO: Delete associated default permission sets on project delete
class ProjectPermissionSet(models.Model):
    """
    Each project has it's own set of permissions.  There are two types, the default permissions
    which are defined when a project is created.  These can be editing and provide the rules for
    anonymous access.
    Each member of a project can also have their own permissions that allow them to do extra tasks.
    """
    is_default = models.BooleanField(default=False) #this should be true if it's a default permission set for a project, otherwise false

    user = models.ForeignKey(User, null=True, blank=True) #this should be null if it's a default permission set for a project
    project = models.ForeignKey(Project)

    push = models.BooleanField(default=False)
    pull = models.BooleanField(default=True)

    add_repos = models.BooleanField(default=False)
    delete_repos = models.BooleanField(default=False)
    edit_repos = models.BooleanField(default=False)
    view_repos = models.BooleanField(default=True)

    add_issues = models.BooleanField(default=True)
    delete_issues = models.BooleanField(default=False)
    edit_issues = models.BooleanField(default=False)
    view_issues = models.BooleanField(default=True)
    
    def __unicode__(self):
        if self.is_default:
            return "Default permission set for project %s" % self.project.longname
        else:
            return "Permissions for %s in %s" % (self.user.username, self.project.longname)

    class Admin:
        list_display = ('__unicode__', 'is_default','push','pull','add_repos','delete_repos','edit_repos','view_repos','add_issues','delete_issues','edit_issues', 'view_issues')
        list_filter = ['is_default', 'project']
