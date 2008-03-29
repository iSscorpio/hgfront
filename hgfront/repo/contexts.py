import datetime

from django.template import Context
from hgfront.repo.models import Repo

def repo_stats(request):
    """
    This function returns the number of repos
    """
    past24 = datetime.datetime.now() - datetime.timedelta(days=1)
    
    return dict([
            ('hgf_num_repos', Repo.objects.all().count()),
            ('hgf_num_repos_last_24_hours', Repo.objects.filter(local_creation_date__gt=past24).count()),
        ])
