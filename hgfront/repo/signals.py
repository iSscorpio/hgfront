# General Libraries
import datetime, sys, os, shutil
from mercurial import hg, ui
# Django Libraries
from django.template import Context, loader
from django.conf import settings
# Project Libraries

def create_repo(sender, instance, signal, *args, **kwargs):
    """Create the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(name_long=instance.project)
    u = ui.ui()
    directory = os.path.join(settings.MERCURIAL_REPOS, p.name_short, instance.repo_dirname)
    
    if not bool(os.path.isdir(directory)):
        #TODO: This is a temporary hack. For some reason instance.creation_method is of type `unicode` while it should be
        # a normal int. I don't know why it's getting it in unicode though.
        creation_method = int(instance.creation_method)
        if creation_method==1:
            hg.repository(u, directory , create=True)
            return True
        elif creation_method==2:
            hg.clone(u, str(instance.repo_url), str(directory), True)
            return True
        else:
            raise ValueError("Invalid Creation Method")
    else:
        raise ValueError("Invalid: %s already exists for this project" % instance.repo_dirname)
    
def move_repo():
    """TODO: Have code that checks if a project has changed in the DB and needs moved"""
    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(name_long=instance.project)
    directory = os.path.join(settings.MERCURIAL_REPOS, p.name_short, instance.repo_dirname)
    if bool(os.path.isdir(directory)):
        return bool(shutil.rmtree(directory))
