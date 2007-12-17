from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    owner = User.objects.get(username=instance.user_posted)
    email = EmailMessage(instance.title, instance.body, settings.ISSUE_FROM_EMAIL, owner.email)
    email.send(False)
