from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from mercurial import hg, ui
from django.conf import settings

import datetime, sys, os, shutil

# Create your models here.
class Project(models.Model):
    longname=models.CharField(max_length=255)
    shortname=models.CharField(max_length=50)
    description=models.TextField()
    private=models.BooleanField(default=False)
    user=models.ForeignKey(User)
    class Admin:
        pass
    
class Repo(models.Model):
    name=models.CharField(max_length=20)
    project=models.ForeignKey(Project)
    def save(self):
        """Call for the creation of a repo first before saving model"""
        self.create_repo()
        super(Repo, self).save()
    def delete(self):
        """Delete the repo first before the model"""
        self.remove_repo()
        super(Repo, self).delete()
    def create_repo(self):
        """Create the mercurial repo"""
        u = ui.ui()
        return bool(hg.repository(u, settings.MERCURIAL_REPOS + self.name, create=True))
    def remove_repo(self):
        """Destroy the mercurial repo"""
        return bool(shutil.rmtree(settings.MERCURIAL_REPOS + self.name))
    class Admin:
        pass