# General Libraries
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Project Libraries

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
    """When a issue is added or changed, email the owner"""
    from issue.models import Issue
    try:
        owner = instance.user_posted
    
        email_body = render_to_string("issue/email/issue.txt",
            {
                'issue_type': instance.issue_type,
                'issue_sev': instance.issue_sev,
                'issue_status': instance.issue_status,
                'issue_raised_by': instance.user_posted,
                'issue_assigned_to': owner.username,
                'issue_message': instance.body
            }
        )
    
        email = EmailMessage(instance.title, email_body, Issue.issue_options.issue_from_email, [owner.email])
        try:
            email.send()
        except:
            pass
    except User.DoesNotExist:
        pass
    else:
        print "Email sent to %s" % owner.email
        
        
        
        
        

