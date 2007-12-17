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
    
    if not bool(os.path.isdir(directory)):
        if instance.creation_method=='1':
            hg.repository(u, directory , create=True)
            create_hgrc(instance, p, directory)
            return True
        elif instance.creation_method=='2':
            hg.clone(u, str(instance.url), directory, True)
            create_hgrc(instance, p, directory)
            return True
        else:
            raise ValueError("Invalid value: %r" % self.creation_method)
    else:
        raise ValueError("Invalid: %s already exists for this project" % self.repo_dirname)
    
def move_repo():
    """TODO: Have code that checks if a project has changed in the DB and needs moved"""
    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    p = Project.objects.get(name_long=instance.project)
    directory = str(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    if bool(os.path.isdir(directory)):
        return bool(shutil.rmtree(directory))
    
def create_hgrc(repo, project, directory):
    """This function outputs a hgrc file within a repo's .hg directory, for use with hgweb"""
    hgrc = open(directory + '/.hg/hgrc', 'w')
    hgrc.write("[web]\n")
    hgrc.write("style = gitweb\n")
    hgrc.write("description = %s\n" % repo.repo_description)
    hgrc.write("contact = %s\n" % project.user_owner)
    a = "allow_archive = "
    if repo.offer_zip:
        a += "zip "
    if repo.offer_tar:
        a += "gz "
    if repo.offer_bz2:
        a += "bz2"
    hgrc.write(a)
    hgrc.close()
