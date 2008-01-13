# General Libraries
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Project Libraries

# Project signals
pre_issue_save = object()
pre_issue_delete = object()
post_issue_save = object()
post_issue_delete = object()

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    owner = User.objects.get(username=instance.user_posted)
    email = EmailMessage(instance.title, instance.body, settings.ISSUE_FROM_EMAIL, [owner.email])
    email.send()
    print "Email sent to %s" % owner.email
