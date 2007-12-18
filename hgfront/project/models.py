# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
from hgfront.project.signals import *

class Project(models.Model):
    """
    A project represents a way to group users, repositories and issues on the system.
    Each project has a project owner who has full control over all aspects of the project.  When
    a project is created, it is also given a default set of permissions for non-members, which are
    changeable
    
    You can also assign members to a project, and give them each their own permission set.
    """
    name_short=models.CharField(max_length=50, db_index=True)
    name_long=models.CharField(max_length=255)
    description_short=models.CharField(max_length=255, blank=True, null=True)
    description_long=models.TextField()
    user_owner=models.ForeignKey(User, related_name='user_owner', verbose_name='project owner')
    user_members=models.ManyToManyField(User, related_name='user_members', verbose_name='project members', null=True, blank=True)
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    is_private=models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name_long

    def num_repos(self):
        """Returns the number of repositories linked to this project"""
        return self.repo_set.count()
    num_repos.short_description = "Number of Repositories"

    def user_in_project(self, user):
        return len(self.user_members.filter(id = user.id)) > 0

    def get_permissions(self, user):
        """ Returns an ProjectPermissionSet of the user `user`.
        If the user is the owner, he gets all permissions.
        If the user has a permissions in the project, return those.
        If the user doesn't have permissions in the project, return
        the default project ones. If those aren't found, returns None
        Also this method adds another property, which is view_project
        This checks against the project's is_private field to see if the 
        user can view the project at all"""
        if user.id == self.user_owner.id:
            permissions = ProjectPermissionSet(is_default=False, user=user, project=self, push=True, pull=True, \
            add_repos = True, delete_repos = True, edit_repos = True, view_repos = True, add_issues = True, \
            delete_issues = True, edit_issues = True, view_issues = True)
        else:
            try:
                permissions = ProjectPermissionSet.objects.get(user__id=user.id, project__id=self.id)
            except ProjectPermissionSet.DoesNotExist, MultipleObjectsReturned:
                permission_list = ProjectPermissionSet.objects.filter(is_default=True, project__id=self.id)
                if len(permission_list) > 0:
                    permissions = permission_list[0]
                else:
                    permissions = None
        permissions.view_project = not self.is_private or self.user_in_project(user) or (self.user_owner.id == user.id)
        return permissions

    def get_absolute_url(self):
        """Creates a permalink to the project page"""
        return ('project-detail', (), {
            "slug": self.name_short
            })

    get_absolute_url = permalink(get_absolute_url)

    class Admin:
        fields = (
                  ('Project Creation', {'fields': ('name_long', 'name_short', 'description_short', 'description_long')}),
                  ('Date information', {'fields': ('pub_date',)}),
                  ('Publishing Details', {'fields': ('user_owner', 'user_members', 'is_private',)}),
        )
        list_display = ('name_long', 'name_short', 'num_repos', 'is_private', 'user_owner', 'pub_date',)
        list_filter = ['pub_date', 'is_private']
        search_fields = ['name_long', 'description']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)


# Dispatchers
dispatcher.connect( create_default_permission_set, signal=signals.post_save, sender=Project )
dispatcher.connect( create_project_dir , signal=signals.post_save, sender=Project )
dispatcher.connect( delete_project_dir , signal=signals.post_delete, sender=Project )

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

    add_repos = models.BooleanField(default=False)
    delete_repos = models.BooleanField(default=False)
    edit_repos = models.BooleanField(default=False)
    view_repos = models.BooleanField(default=True)

    add_issues = models.BooleanField(default=True)
    delete_issues = models.BooleanField(default=False)
    edit_issues = models.BooleanField(default=False)
    view_issues = models.BooleanField(default=True)
    
    add_wiki = models.BooleanField(default=True)
    delete_wiki = models.BooleanField(default=False)
    edit_wiki = models.BooleanField(default=False)
    view_wiki = models.BooleanField(default=True)
    
    def __unicode__(self):
        if self.is_default:
            return "Default permission set for project %s" % self.project.name_long
        else:
            return "Permissions for %s in %s" % (self.user.username, self.project.name_long)

    class Admin:
        list_display = ('__unicode__', 'is_default',)
        list_filter = ['is_default', 'project']
