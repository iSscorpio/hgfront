# Django Libraries
from django.conf import settings
from django.db.models import get_models, signals
from django.dispatch import dispatcher

def create_queues(app, created_models, verbosity, **kwargs):
    """This creates the initial queues that mercural manager works with"""
    from repo.models import Queue
    if Queue in created_models:
        Queue.objects.get_or_create(name='repoclone')
        Queue.objects.get_or_create(name='repoupdate')
        
# Dispatchers       
signals.post_syncdb.connect(create_queues)