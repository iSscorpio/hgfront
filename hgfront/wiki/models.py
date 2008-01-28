from django.db import models
from hgfront.project.models import Project

class Page(models.Model):
    parent_project = models.ForeignKey(Project)
    name = models.CharField(max_length=255, primary_key=True)
    content = models.TextField(blank=True)
    
    class Meta:
        unique_together=('parent_project','name')
