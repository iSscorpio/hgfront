from django.db import models
from hgfront.project.models import Project

class Page(models.Model):
    parent_project = models.ForeignKey(Project)
    name = models.CharField(max_length=255, primary_key=True)
    content = models.TextField(blank=True)

    def __unicode__(self):
        page_name = ' '.join( self.name.split( '_' ) ).title()
        return self.parent_project.name_long + ' / ' + page_name
        
    def changesets(self):
        changes = PageChange.objects.filter(page_id=self.name)
        if changes:
            return changes
        else:
            return "There are no changesets"

    class Admin:
        pass

    class Meta:
        unique_together=('parent_project','name')
        
class PageChange(models.Model):
    page_id = models.ForeignKey(Page)
    change_message = models.CharField(max_length=255)

    def __unicode__(self):
        return "Changeset for " + self.page_id.parent_project.name_short + ' / ' + self.page_id.name 

    class Admin:
        pass
