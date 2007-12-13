from django.template import Context, loader
from django.conf import settings
from mercurial import hg, ui

import datetime, sys, os, shutil

def create_project_dir(sender, instance, signal, *args, **kwargs):
    return bool(shutil.os.mkdir(settings.MERCURIAL_REPOS + instance.shortname))

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    return bool(shutil.rmtree(settings.MERCURIAL_REPOS + instance.shortname))

def create_repo(sender, instance, signal, *args, **kwargs):
    """Create the mercurial repo"""
    from hgfront.project.models import Project, Repo
    p = Project.objects.get(longname=instance.project)
    u = ui.ui()
    if instance.creation_method=='1':
        return bool(hg.repository(u, str(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name), create=True))
    elif self.creation_method=='2':
        return bool(hg.clone(u, str(instance.url), str(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name), True))
    else:
        raise ValueError("Invalid value: %r" % self.creation_method)
    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    from hgfront.project.models import Project, Repo
    p = Project.objects.get(longname=instance.project)
    return bool(shutil.rmtree(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name))
