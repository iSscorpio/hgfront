# General Libraries
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Project Libraries

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    from hgfront.issue.models import Issue
    try:
        owner = instance.user_posted
        
        message = """
            Issue Type: %s \n
            Issue Severity: %s \n
            Issue Status: %s \n
            \n
            User Raised: %s \n
            User Assigned To: %s \n
            \n
            Issue Message: %s
            """ % (instance.issue_type, instance.issue_sev, instance.issue_status, instance.user_posted, owner.username, instance.body)
            
        
        email = EmailMessage(instance.title, message, Issue.issue_options.issue_from_email, [owner.email])
        try:
            email.send()
        except:
            pass
    except User.DoesNotExist:
        pass
    else:
        print "Email sent to %s" % owner.email
