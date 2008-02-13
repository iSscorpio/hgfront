from django.db import models
import datetime, os
from hgfront.project.models import Project

# Create your models here.

class ProjectBackup(models.Model):
    parent_project=models.ForeignKey(Project)
    format=models.CharField(max_length=10)
    created=models.DateTimeField()
    expires=models.DateTimeField(null=True,blank=True)
    file_path = models.TextField()
    file_name = models.CharField(max_length=255)
    
    class Admin:
        pass
