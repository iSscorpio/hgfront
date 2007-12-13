from django.template import Context, loader
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

def init_issues_types(sender, instance, signal, *args, **kwargs):
    """This injects the database with default values for issues"""
    issue_types = (
        ('Bug', 0,),
        ('Enhancment', 1,),
        ('Feature Request', 2,),
        ('Typo', 3,)
    )
    for issue in issue_types:
        p = sender(title = issue[0], order=issue[1])
        p.save()
        
def init_issues_sevs(sender, instance, signal, *args, **kwargs):
    """This injects the database with default values for issues"""
    sev_types = (
        ('Minor', 0,),
        ('Medium', 1,),
        ('Major', 2,),
        ('Critical', 3,),
        ('Blocker', 4,)
    )
    for sev in sev_types:
        s = sender(title = sev[0], order=sev[1])
        s.save()
        
def init_issues_status(sender, instance, signal, *args, **kwargs):
    """This injects the database with default values for issues"""
    status_types = (
        ('Raised', 0,),
        ('Accepted', 1,),
        ('Not Accepted', 2,),
        ('Fixed', 3,),
        ('Works For Me', 4,)
    )
    for status in status_types:
        t = sender(title = status[0], order=status[1])
        t.save()

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    owner = User.objects.get(username=instance.user_assigned_to)
    email = EmailMessage(instance.title, instance.body, settings.ISSUE_FROM_EMAIL, owner.email)
    email.send(False)