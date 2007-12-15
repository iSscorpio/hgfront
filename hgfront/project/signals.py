from django.template import Context, loader
from django.conf import settings

import datetime, sys, os, shutil

def create_default_permission_set(sender, instance, signal, *args, **kwargs):
    from hgfront.project.models import Project, ProjectPermissionSet
    permission_set = ProjectPermissionSet(is_default=True, project=instance, user=None)
    permission_set.save()

def create_project_dir(sender, instance, signal, *args, **kwargs):
    path = os.path.isdir(settings.MERCURIAL_REPOS + instance.shortname)
    if path is False:
        return bool(shutil.os.mkdir(settings.MERCURIAL_REPOS + instance.shortname))

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    path = os.path.isdir(settings.MERCURIAL_REPOS + instance.shortname)
    if path is True:
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + instance.shortname))