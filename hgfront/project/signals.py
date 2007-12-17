from django.template import Context, loader
from django.conf import settings

import datetime, sys, os, shutil

def create_default_permission_set(sender, instance, signal, *args, **kwargs):
    """
    Executed on creation of a project, this defines the default permissions
    """
    from hgfront.project.models import Project, ProjectPermissionSet
    existing = ProjectPermissionSet.objects.filter(project__id = instance.id, is_default=True)
    if not existing:
        permission_set = ProjectPermissionSet(is_default=True, project=instance, user=None)
        permission_set.save()

def create_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path already exists, and if not this is a new project so creates path.
    """
    if not bool(os.path.isdir(settings.MERCURIAL_REPOS + instance.name_short)):
        return bool(shutil.os.mkdir(settings.MERCURIAL_REPOS + instance.name_short))

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path still exists for project and if it does, deletes it.
    """
    if bool(os.path.isdir(settings.MERCURIAL_REPOS + instance.name_short)):
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + instance.name_short))
