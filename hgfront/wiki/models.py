from django.db import models
from hgfront.project.models import Project

class Page(models.Model):
    parent_project = models.ForeignKey(Project)
    name = models.CharField(max_length=255, primary_key=True)
    content = models.TextField(blank=True)

    def __unicode__(self):
        page_name = ' '.join( self.name.split( '_' ) ).title()
        return self.parent_project.name_long + '/' + page_name

    class Admin:
        pass

    class Meta:
        unique_together=('parent_project','name')

class PageChange(models.Model):
    page_id = models.ForeignKey(Page)
    change_message = models.CharField(max_length=255)

    class Admin:
        pass
