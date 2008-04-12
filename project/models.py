# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
from core.configs import ProjectOptions
from project.signals import *

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

    def request_to_join(self, project, user):
        """
        This makes a ProjectPermissionSet for the project `project` with the user `user` and it's set so it's
        accepted by the user but not the project.
        """
        ProjectPermissionSet(is_default=False, user_accepted=True, owner_accepted=False, user=user, project=project).save()


class Project(models.Model):
    """
    The Project model is the core model of Mercurial Manager.
    
    Project allows repositories to be collected into a single group representing an
    application, as well as handle all it's members with their permissions and issues
    
    The project model will provide a way to hook in other applications around each other.
    
    Each project has a project owner who has full control over all aspects of the project.  When
    a project is created, it is also given a default set of permissions for non-members, which are
    changeable.
    Members are assigned to projects by giving them permissions on the project.
    """
    # Define the available styles for hgweb
    AVAILABLE_STYLES = [(x, x) for x in ("Default", "Gitweb",)]

    # project_id: This is a slugfield with a unique name for the project, there can be no other projects with the same name
    project_id=models.SlugField(unique=True, editable=False)
    # project_name: This is the human-readable name of the project
    project_name=models.CharField(max_length=255)
    # short_description: This is the short description of a project for RSS feeds, widgets, lists, etc
    short_description=models.CharField(max_length=255, blank=True, null=True)
    # full_description: This is the full freetext description of the project
    full_description=models.TextField()
    # project_icon: This is the icon used to give the project some visual air
    project_icon = models.ImageField(upload_to='project_icons', blank=True, null=True)
    # project_manager: This is the person managing the project on this instance of hgmanager
    project_manager=models.ForeignKey(User, related_name='project_manager', verbose_name='project manager')
    # hgweb_style: The style to apply to the hgweb application
    hgweb_style=models.CharField(max_length=50,choices=AVAILABLE_STYLES)
    # created_date: The date the project instance was created
    created_date=models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created on')
    # modified_date: The date the project instance was last modified
    modified_date=models.DateTimeField(auto_now=True, editable=False, verbose_name='last updated')

    # Model properties
    
    # Define the object type for the model
    projects = ProjectManager()    
    # Define the model options
    project_options = ProjectOptions()

    # Define the Meta class
    class Meta:
        ordering = ['project_name',]
        get_latest_by = 'modified_date'
        permissions = (
            ("can_create_project", "Can Create Project"),
            ("can_read_project", "Can Read Project"),
            ("can_update_project", "Can Update Project"),
            ("can_delete_project", "Can Delete Project"),
        )
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    # Define the Admin class
    class Admin:
        fields = (
                  ('Project Details', {'fields':
                                        ('project_id',
                                         'project_name',
                                         'short_description',
                                         'full_description',
                                         'project_icon',
                                         )
                                        }
                  ),
                  ('Date information', {'fields':
                                        ('created_date',
                                         'modified_date'
                                         )
                                        }
                  ),
                  ('Publishing Details', {'fields':
                                          ('hgweb_style',
                                           'project_manager',
                                           )
                                          }
                  ),
        )
        list_display = (
                        'project_name',
                        'short_description',
                        'project_manager',
                        'number_of_repos',
                        'created_date',
                        'modified_date',
                        )
        list_filter = ['created_date','modified_date',]
        search_fields = ['project_name', 'short_description', 'full_description',]
        date_hierarchy = 'created_date'
        ordering = ('created_date', 'project_id',)

    # Model Methods        
    def __unicode__(self):
        return self.project_name

    def number_of_repos(self):
        """Returns the number of repositories linked to this project"""
        return self.repo_set.count()
    number_of_repos.short_description = "No. Repositories"
    number_of_repos = property(number_of_repos)
    
    def total_size(self):
        filesize = 0
        for r in self.repo_set.all():
            filesize += r.folder_size
        return filesize
    total_size = property(total_size)
    
    def number_of_members(self):
        """Returns the total number of members including the owner"""
        return self.user_set.count()
    number_of_members.short_description = "No. Members"
    number_of_members = property(number_of_members)
    
    def project_directory(self):
        return os.path.join(Project.project_options.repository_directory, self.project_id)
    project_directory.short_description = "Project Path"
    project_directory = property(project_directory)
    
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
        if user.id == self.project_manager.id:
            permissions = ProjectPermissionSet.objects.get_owner_permission_set(user, self)
        else:
            try:
                #Try to find a permission set for the user
                permissions = self.projectpermissionset_set.get(user__id=user.id, user_accepted = True, owner_accepted = True)
            except ProjectPermissionSet.DoesNotExist:
                #If there's no specific permission set for the user, try to find a default permission set
                try:
                    permissions = self.get_default_permissionset()
                except ProjectPermissionSet.DoesNotExist:
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
        default_permission_list = self.projectpermissionset_set.filter(is_default=True)
        if len(default_permission_list) == 0:
            raise ProjectPermissionSet.DoesNotExist
        else:
            return default_permission_list[0]

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
        return ('project-detail', (), { "slug": self.project_id })


# Dispatchers
dispatcher.connect( create_default_permission_set, signal=signals.post_save, sender=Project )
dispatcher.connect( create_project_dir, signal=signals.post_save, sender=Project )
dispatcher.connect( create_hgwebconfig, signal=signals.post_save, sender=Project )
dispatcher.connect( send_email_to_owner, signal=signals.post_save, sender=Project )
dispatcher.connect( create_wikipage, signal=signals.post_save, sender=Project )
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
        

class ProjectNews(models.Model):
    parent_project=models.ForeignKey(Project)
    news_title=models.CharField(max_length=255)
    news_body=models.TextField()
    published=models.BooleanField(default=True)
    frontpage=models.BooleanField(default=False)
    authorised=models.BooleanField(default=False)
    pub_date=models.DateTimeField()
    
    news_items = models.Manager()
    
    def __unicode__(self):
        return self.parent_project.name_long + ' / ' + self.news_title
    
    class Admin:
        pass
        
    class Meta:
        verbose_name = 'project news item'
        verbose_name_plural = 'project news items'
        ordering = ['pub_date', 'parent_project']

