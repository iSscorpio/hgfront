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
    from hgfront.config.models import SiteOptions
    d = SiteOptions.objects.get(option_key__exact = 'repo_location')
    if not bool(os.path.isdir(os.path.join(d.option_value, instance.name_short))):
        return bool(shutil.os.mkdir(os.path.join(d.option_value ,instance.name_short)))

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path still exists for project and if it does, deletes it.
    """
    from hgfront.config.models import SiteOptions
    d = SiteOptions.objects.get(option_key__exact = 'repo_location')
    
    if bool(os.path.isdir(os.path.join(d.option_value, instance.name_short))):
        return bool(shutil.rmtree(os.path.join(d.option_value, instance.name_short)))

def create_hgwebconfig(sender, instance, signal, *args, **kwargs):
    """
    Creates a hgweb.config file for use with hgwebdir
    """
    from hgfront.config.models import InstalledStyles, SiteOptions
    s = InstalledStyles.objects.get(short_name = instance.hgweb_style)
    d = SiteOptions.objects.get(option_key__exact = 'repo_location')
    directory = os.path.join(d.option_value, instance.name_short)
    if bool(os.path.isdir(directory)):
        config = open(os.path.join(directory, 'hgweb.config'), 'w')
        config.write('[collections]\n')
        config.write('%s = %s\n\n' % (directory, directory))
        config.write('[web]\n')
        config.write('style = %s' % s.short_name)
        config.close()
        shutil.copy(os.path.join(settings.HGFRONT_TEMPLATES_PATH, 'project/hgwebdir.txt'), os.path.join(d.option_value, instance.name_short, 'hgwebdir.cgi'))
        os.chmod(os.path.join(d.option_value, instance.name_short, 'hgwebdir.cgi'), 0755)
        return True
