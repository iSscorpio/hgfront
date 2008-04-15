# General Libraries
import datetime, sys, os, shutil
from mercurial import hg, ui
# Django Libraries
from django.template import Context, loader
from django.conf import settings
from core.libs.json_libs import json_encode
# Project Libraries

def create_repo(sender, instance, signal, *args, **kwargs):
    """Create the mercurial repo"""    
    if not bool(os.path.isdir(instance.repo_directory())):
        creation_method = int(instance.creation_method)
        if creation_method==1:
            u = ui.ui()
            hg.repository(u, instance.repo_directory() , create=True)
            return True
        elif creation_method==2:
            q = Queue.objects.get(name='createrepos')
            
            clone = json_encode(instance)
            
            msg = Message(message=clone, queue=q)
            msg.save()
            #hg.clone(u, str(instance.default_path), str(instance.repo_directory()), True)
            return True
        else:
            raise ValueError("Invalid Creation Method")
    else:
        raise ValueError("Invalid: %s already exists for this project" % instance.name_short)
    
def move_repo():
    """TODO: Have code that checks if a project has changed in the DB and needs moved"""
    
def delete_repo(sender, instance, signal, *args, **kwargs):
    """Destroy the mercurial repo"""
    if bool(os.path.isdir(instance.repo_directory)):
        return bool(shutil.rmtree(instance.repo_directory))
    
def get_repo_size(sender, instance, signal, *args, **kwargs):
    instance.folder_size = 0
    for (path, dirs, files) in os.walk(instance.repo_directory):
        for file in files:
            filename = os.path.join(path, file)
            instance.folder_size += os.path.getsize(filename)
