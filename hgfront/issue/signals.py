# General Libraries
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Project Libraries

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    try:
        owner = User.objects.get(username=instance.user_posted)
        email = EmailMessage(instance.title, instance.body, settings.ISSUE_FROM_EMAIL, [owner.email])
        email.send()
    except User.DoesNotExist:
        pass
    else:
        print "Email sent to %s" % owner.email
