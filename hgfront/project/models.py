# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
from hgfront.config.models import InstalledStyles
from hgfront.project.signals import *

class ProjectManager(models.Manager):
    """
    Manager class for Project.
    """
    def projects_for_user(self, user):
        """
        This returns a list of projects that the user `user` is in and has
        accepted. This is the prefered way of getting all the projects that
        the user is in. Ideally this functionality should be a method of the
        User class but I think extending the User class just for this would
        overcomplicate things
        """
        return self.filter(
            projectpermissionset__user = user, 
            projectpermissionset__is_default = False,
            projectpermissionset__user_accepted = True,
            projectpermissionset__owner_accepted = True
        )

    def project_invitations(self, user):
        """
        This returns a list of projects that the user `user` has yet to accept
        """
        return self.filter(projectpermissionset__user = user, projectpermissionset__user_accepted = False)

    def project_join_requests(self, user):
        """
        This returns a list of projects that the user `user` has applied to join but haven't been approved yet.
        """
        return self.filter(projectpermissionset__user = user, projectpermissionset__owner_accepted = False)


class Project(models.Model):
    """
    A project represents a way to group users, repositories and issues on the system.
    Each project has a project owner who has full control over all aspects of the project.  When
    a project is created, it is also given a default set of permissions for non-members, which are
    changeable.
    Members are assigned to projects by giving them permissions on the project.
    """
    name_short=models.CharField(max_length=50, db_index=True, unique=True)
    name_long=models.CharField(max_length=255)
    description_short=models.CharField(max_length=255, blank=True, null=True)
    description_long=models.TextField()
    user_owner=models.ForeignKey(User, related_name='user_owner', verbose_name='project owner')
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    hgweb_style=models.ForeignKey(InstalledStyles)

    objects = ProjectManager()
    
    def __unicode__(self):
        return self.name_long

    def num_repos(self):
        """Returns the number of repositories linked to this project"""
        return self.repo_set.count()
    num_repos.short_description = "Number of Repositories"

    def user_in_project(self, user):
        return len(self.members.filter(id = user.id)) > 0

    def get_permissions(self, user):
        """ Returns an ProjectPermissionSet of the user `user`.
        If the user is the owner, he gets all permissions.
        If the user has a permission set in the project, return those.
        If the user doesn't have permissions in the project, return
        the default project ones. If those aren't found, returns a
        permission set with all the permissions set to False.
        """
        #if the user is the owner of the project, give him all permissions
        if user.id == self.user_owner.id:
            permissions = ProjectPermissionSet.objects.get_owner_permission_set(user, self)
        else:
            try:
                #Try to find a permission set for the user
                permissions = self.projectpermissionset_set.get(user__id=user.id, user_accepted = True, owner_accepted = True)
            except ProjectPermissionSet.DoesNotExist:
                #If there's no specific permission set for the user, try to find a default permission set
                permission_list = self.projectpermissionset_set.filter(is_default=True)
                if len(permission_list) > 0:
                    permissions = permission_list[0]
                else:
                    #If even a default one isn't found (although this shouldn't happen), return a restricted permission set
                    permissions = ProjectPermissionSet.objects.get_null_permission_set(user, self)
        return permissions

    def _get_members(self):
        """
        Gets the QuerySet of the project's users. It gets them via the
        project's permission sets. Basically one permission set means one
        user to the project. To access this just use:

        project.members

        Because it returns a QuerySet, you can treat it like you would any
        QuerySet. For example:

        project.members.filter(id=1)

        """
        return User.objects.filter (
            projectpermissionset__project__id = self.id, 
            projectpermissionset__is_default = False,
            projectpermissionset__user_accepted = True,
            projectpermissionset__owner_accepted = True
        )
    members = property(_get_members)

    def _get_invited_members(self):
        """
        Gets the QuerySet of the users that have been invited to join the project but haven't accepted their invitation yet
        """
        return User.objects.filter(projectpermissionset__project__id = self.id, projectpermissionset__is_default = False, projectpermissionset__user_accepted = False)
    invited_members = property(_get_invited_members)

    def _get_aspiring_members(self):
        """
        Gets the QuerySet of the users that have requested to join the project but whose requests haven't been approved
        by the project owner.
        """
        return User.objects.filter(projectpermissionset__project__id = self.id, projectpermissionset__is_default = False, projectpermissionset__owner_accepted = False)
    aspiring_members = property(_get_aspiring_members)

    def is_private(self):
        return not self.get_default_permissionset().view_project

    def get_default_permissionset(self):
        return self.projectpermissionset_set.filter(is_default=True)[0]

    def accept_join_request(self, permissionset):
        """
        This method takes a permissionset that has yet to be approved by the owner and approves it.
        Basically it approves a user's request to join a project.

        The procedure of approving a permissionset is
        1. The owner_accepted flag is set to True
        2. The permissions are set to the project's default permission set, which the owner
        will later probably want to change
        """

        # What's basically achieved here is that the permission set for the aspiring
        # member of the project gets all the permissions from the project's permission
        # set and then it gets the owner_accepted flag set to false.
        # permission set of the user who wants to join
        defaultpermissionset = self.get_default_permissionset()
        newpermissionset = defaultpermissionset
        newpermissionset.id = permissionset.id
        newpermissionset.user = permissionset.user
        newpermissionset.user_accepted = permissionset.user_accepted
        newpermissionset.owner_accepted = True
        newpermissionset.is_default = False
        newpermissionset.save()

    @permalink
    def get_absolute_url(self):
        """Creates a permalink to the project page"""
        return ('project-detail', (), { "slug": self.name_short })

    class Admin:
        fields = (
                  ('Project Creation', {'fields': ('name_long', 'name_short', 'description_short', 'description_long')}),
                  ('Date information', {'fields': ('pub_date',)}),
                  ('Publishing Details', {'fields': ('hgweb_style', 'user_owner',)}),
        )
        list_display = ('name_long', 'name_short', 'num_repos', 'is_private', 'user_owner', 'pub_date',)
        list_filter = ['pub_date',]
        search_fields = ['name_long', 'description']
        date_hierarchy = 'pub_date'
        ordering = ('pub_date',)


# Dispatchers
dispatcher.connect( create_default_permission_set, signal=signals.post_save, sender=Project )
dispatcher.connect( create_project_dir, signal=signals.post_save, sender=Project )
dispatcher.connect( create_hgwebconfig, signal=signals.post_save, sender=Project )
dispatcher.connect( delete_project_dir, signal=signals.post_delete, sender=Project )

class ProjectPermissionSetManager(models.Manager):
    """
    A manager for project permission sets.
    """
    def get_owner_permission_set(self, user, project):
        """
        Returns a permission set with full permissions for the user `user` in project `project`
        """
        return ProjectPermissionSet(is_default=False, user=user, project=project,\
        view_project = True, edit_project= True, add_members=True, delete_members = True,\
        add_repos = True, delete_repos = True, edit_repos = True, view_repos = True,\
        add_issues = True, delete_issues = True, edit_issues = True, view_issues = True, \
        add_wiki = True, delete_wiki = True, edit_wiki = True, view_wiki = True)
    
    def get_null_permission_set(self, user, project):
        """
        Returns a permission set with no permissions for the user `user` in project `project`
        Only to be used in case a project doesn't have a default permission set, although that
        normally shouldn't happen
        """
        return ProjectPermissionSet(is_default=False, user=user, project=project,\
        view_project = False, edit_project= False, add_members=False, delete_members = False,\
        add_repos = False, delete_repos = False, edit_repos = False, view_repos = False,\
        add_issues = False, delete_issues = False, edit_issues = False, view_issues = False, \
        add_wiki = False, delete_wiki = False, edit_wiki = False, view_wiki = False)

class ProjectPermissionSet(models.Model):
    """
    Each project has its own set of permissions.  There are two types, the default permissions
    which are defined when a project is created.  These can be editing and provide the rules for
    anonymous access.
    Each member is connected to the project via the permission set that it has for that project.
    """
    is_default = models.BooleanField(default=False) #this should be true if it's a default permission set for a project, otherwise false

    user_accepted = models.BooleanField(default=True) #whether the user has accepted to be in the project
    owner_accepted = models.BooleanField(default=True) #whether the owner has accepted that the user can be in the project

    user = models.ForeignKey(User, null=True, blank=True) #this should be null if it's a default permission set for a project
    project = models.ForeignKey(Project)

    view_project = models.BooleanField(default=True)
    edit_project = models.BooleanField(default=False)

    add_members = models.BooleanField(default=False)
    delete_members = models.BooleanField(default=False)

    add_repos = models.BooleanField(default=False)
    delete_repos = models.BooleanField(default=False)
    edit_repos = models.BooleanField(default=False)
    view_repos = models.BooleanField(default=True)

    add_issues = models.BooleanField(default=False)
    delete_issues = models.BooleanField(default=False)
    edit_issues = models.BooleanField(default=False)
    view_issues = models.BooleanField(default=True)
    
    add_wiki = models.BooleanField(default=False)
    delete_wiki = models.BooleanField(default=False)
    edit_wiki = models.BooleanField(default=False)
    view_wiki = models.BooleanField(default=True)

    objects = ProjectPermissionSetManager()
    
    def __unicode__(self):
        if self.is_default:
            return "Default permission set for project %s" % self.project.name_long
        else:
            return "Permissions for %s in %s" % (self.user.username, self.project.name_long)

    class Admin:
        list_display = ('__unicode__', 'is_default',)
        list_filter = ['is_default', 'project']
    
    class Meta:
        unique_together = ('user','project')
