"""
Creates default values for the Issue tracker
"""
# General Libraries
# Django Libraries
from django.conf import settings
from django.db.models import get_models, signals
from django.dispatch import dispatcher
# Project Libraries

def init_issues_types(app, created_models, verbosity, **kwargs):
    """This injects the database with default values for issues"""
    from hgfront.issue.models import IssueType
    if IssueType in created_models:
        IssueType.objects.get_or_create(title='Bug', defaults={'title':'Bug','order': '0', 'is_active': '1'})
        IssueType.objects.get_or_create(title='Enhancment', defaults={'title':'Enhancment','order': '1', 'is_active': '1'})
        IssueType.objects.get_or_create(title='Feature Request', defaults={'title':'Feature Request','order': '2', 'is_active': '1'})
        IssueType.objects.get_or_create(title='Typo', defaults={'title':'Typo','order': '3', 'is_active': '1'})
        
def init_issues_sevs(app, created_models, verbosity, **kwargs):
    """This injects the database with default values for severity"""
    from hgfront.issue.models import IssueSeverity
    if IssueSeverity in created_models:
        IssueSeverity.objects.get_or_create(title='Minor', defaults={'title':'Minor','order': '0', 'is_active': '1'})
        IssueSeverity.objects.get_or_create(title='Medium', defaults={'title':'Medium','order': '1', 'is_active': '1'})
        IssueSeverity.objects.get_or_create(title='Major', defaults={'title':'Major','order': '2', 'is_active': '1'})
        IssueSeverity.objects.get_or_create(title='Critical', defaults={'title':'Critical','order': '3', 'is_active': '1'})
        IssueSeverity.objects.get_or_create(title='Blocker', defaults={'title':'Blocker','order': '4', 'is_active': '1'})
        
def init_issues_status(app, created_models, verbosity, **kwargs):
    """This injects the database with default values for status"""
    from hgfront.issue.models import IssueStatus
    if IssueStatus in created_models:
        IssueStatus.objects.get_or_create(title='Raised', defaults={'title':'Raised','order': '0', 'is_active': '1'})
        IssueStatus.objects.get_or_create(title='Accepted', defaults={'title':'Accepted','order': '1', 'is_active': '1'})
        IssueStatus.objects.get_or_create(title='Not Accepted', defaults={'title':'Not Accepted','order': '2', 'is_active': '1'})
        IssueStatus.objects.get_or_create(title='Fixed', defaults={'title':'Fixed','order': '3', 'is_active': '1'})
        IssueStatus.objects.get_or_create(title='Works For Me', defaults={'title':'Works For Me','order': '4', 'is_active': '1'})

# Dispatchers       
dispatcher.connect(init_issues_types, signal=signals.post_syncdb)
dispatcher.connect(init_issues_sevs, signal=signals.post_syncdb)
dispatcher.connect(init_issues_status, signal=signals.post_syncdb)