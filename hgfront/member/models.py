from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher

# Create your models here.

class Member(models.Model):
    member_user = models.ForeignKey(User)
    member_homepage = models.URLField()
    
    def __unicode__(self):
        return self.member_user.username
    
    class Admin:
        pass