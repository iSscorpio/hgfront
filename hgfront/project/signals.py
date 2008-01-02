# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.template import Context, loader
# Project Libraries

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

def create_hgwebconfig(sender, instance, signal, *args, **kwargs):
    """
    Creates a hgweb.config file for use with hgwebdir
    """
    from hgfront.config.models import InstalledStyles
    s = InstalledStyles.objects.get(short_name = instance.hgweb_style)
    if bool(os.path.isdir(settings.MERCURIAL_REPOS + instance.name_short)):
        config = open(settings.MERCURIAL_REPOS + instance.name_short + '/hgweb.config', 'w')
        config.write('[collections]\n')
        config.write(str(settings.MERCURIAL_REPOS + instance.name_short) + ' = ' + str(settings.MERCURIAL_REPOS + instance.name_short) + '\n\n')
        config.write('[web]\n')
        config.write('style = ' + s.short_name)
        config.close()
        shutil.copy('/home/digitalspaghetti/workspace/hgfront-dev/hgfront/templates/project/hgwebdir.txt', settings.MERCURIAL_REPOS + instance.name_short + '/hgwebdir.cgi')
        os.chmod(settings.MERCURIAL_REPOS + instance.name_short + '/hgwebdir.cgi', 0755)
        return True