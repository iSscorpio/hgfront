from django.template import Context, loader
from django.conf import settings
from mercurial import hg, ui

import datetime, sys, os, shutil

def create_repo(sender, instance, signal, *args, **kwargs):
    """Create the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(longname=instance.project)
    u = ui.ui()
    if instance.creation_method=='1':
        return bool(hg.repository(u, str(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name), create=True))
    elif instance.creation_method=='2':
        return bool(hg.clone(u, str(instance.url), str(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name), True))
    else:
        raise ValueError("Invalid value: %r" % self.creation_method)
    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(longname=instance.project)
    path = os.path.isdir(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name)
    if path is False:
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + p.shortname + '/' + instance.name))