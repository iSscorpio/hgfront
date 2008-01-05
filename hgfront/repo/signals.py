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
    directory = str(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    
    if not bool(os.path.isdir(directory)):
        method = int(instance.creation_method)
        if method==1:
            hg.repository(u, directory , create=True)
            return True
        elif method==2:
            hg.clone(u, str(instance.repo_url), directory, True)
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
    directory = str(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    if bool(os.path.isdir(directory)):
        return bool(shutil.rmtree(directory))
    
def create_hgrc(sender, instance, signal, *args, **kwargs):
    """This function outputs a hgrc file within a repo's .hg directory, for use with hgweb"""
    from hgfront.project.models import Project
    from hgfront.repo.models import Repo
    from django.contrib.auth.models import User
    from hgfront.config.models import InstalledStyles, InstalledExtensions
    p = Project.objects.get(name_long=instance.project)
    c = User.objects.get(username__exact=instance.repo_contact)
    s = InstalledStyles.objects.get(short_name = instance.hgweb_style)
    directory = str(settings.MERCURIAL_REPOS + p.name_short + '/' + instance.repo_dirname)
    
    hgrc = open(directory + '/.hg/hgrc', 'w')
    hgrc.write('[paths]\n')
    hgrc.write('default = %s\n\n' % instance.repo_url)
    hgrc.write('[web]\n')
    hgrc.write('style = %s\n' % s.short_name)
    hgrc.write('description = %s\n' % instance.repo_description)
    hgrc.write('contact = %s <%s>\n' % (c.username, c.email))
    a = 'allow_archive = '
    if instance.offer_zip:
        a += 'zip '
    if instance.offer_tar:
        a += 'gz '
    if instance.offer_bz2:
        a += 'bz2'
    hgrc.write(a + '\n\n')
    hgrc.write('[extensions]')
    # TODO: This doesn't seem to be working :/
    #print instance.active_extensions.all()._get_sql_clause()
    for e in instance.active_extensions.all():
        #print e.short_name
        hgrc.write('hgext.%s = \n' % e.short_name)
    hgrc.close()
