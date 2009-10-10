from django.conf import settings
from django.contrib import admin

admin.autodiscover()

# Project Libraries

urlpatterns = patterns('backup.views',
    url('^$','create_project_backup', name='create-backup'),
    url('^(?P<format>[-\w]+)/$', 'create_project_backup', name='selected-backup'),
	url('^download/(?P<backup_id>[-\d]+)/$', 'download_project_backup', name='download-backup'),
)
