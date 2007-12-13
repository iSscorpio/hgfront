from django.dispatch import dispatcher
from django.db.models import signals

from hgfront.issue.models import *

def init_issues_database():
    """This injects the database with default values for issues"""
    issue_types = (
        ('Bug', 0,),
        ('Enhancment', 1,),
        ('Feature Request', 2,),
        ('Typo', 3,)
    )
    for issue in issue_types:
        p = IssueType(title = issue[0], order=issue[1])
        p.save()
    
    sev_types = (
        ('Minor', 0,),
        ('Medium', 1,),
        ('Major', 2,),
        ('Critical', 3,),
        ('Blocker', 4,)
    )
    for sev in sev_types:
        s = IssueSeverity(title = sev[0], order=sev[1])
        s.save()
        
    status_types = (
        ('Raised', 0,),
        ('Accepted', 1,),
        ('Not Accepted', 2,),
        ('Fixed', 3,),
        ('Works For Me', 4,)
    )
    for status in status_types:
        t = IssueStatus(title = status[0], order=status[1])
        t.save()
        
dispatcher.connect(init_issues_database, signal=signals.post_syncdb)