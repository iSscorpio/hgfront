# General Libraries
import datetime
# Django Libraries
from django.db import models
from django.db.models import permalink
# Project Libraries
from hgfront.project.models import Project

class WikiPage(models.Model):
    """This represents a Wiki Page related to a project"""
    title=models.CharField(max_length=150)
    slug=models.SlugField()
    body=models.TextField(verbose_name='contents')
    pub_date=models.DateTimeField(default=datetime.datetime.now(), verbose_name='created on')
    project=models.ForeignKey(Project)
    
    def __unicode__(self):
        return self.title
    
    def save(self):
        if not self.slug:
            import re
            wikifier = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
            self.slug = wikifier.sub(r'\1', self.title)
        super(WikiPage, self).save()
    def get_absolute_url(self):
        """Creates a permalink to the wiki page"""
        return ('wiki-page', (), {
            "slug": self.project.name_short,
            "page_name": self.slug
            })
    get_absolute_url = permalink(get_absolute_url)
    
    class Admin:
        pass
