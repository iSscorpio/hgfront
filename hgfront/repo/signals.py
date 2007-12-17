from django.template import Context, loader
from django.conf import settings
from mercurial import hg, ui

import datetime, sys, os, shutil

def create_repo(sender, instance, signal, *args, **kwargs):
    """Create the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(name_long=instance.project)
    u = ui.ui()
    
    directory = str(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    
    if instance.creation_method=='1':
        repo = hg.repository(u, directory , create=True)
        if repo:
            hgrc = open(directory + '/.hg/hgrc', 'w')
            hgrc.write("[web]\n")
            hgrc.write("style = gitweb\n")
            hgrc.close()
        else:
            return False
    elif instance.creation_method=='2':
        return bool(hg.clone(u, str(instance.url), directory, True))
    else:
        raise ValueError("Invalid value: %r" % self.creation_method)

    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(name_long=instance.project)
    path = os.path.isdir(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    if path is False:
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname))
