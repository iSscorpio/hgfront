# General Libraries
import datetime, os
from time import strftime
# Django Libraries
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Project Libraries
from backup.models import ProjectBackup
from project.models import Project, ProjectPermissionSet
from project.decorators import check_project_permissions

@login_required
def create_project_backup(request, slug, format='tar'):

    project = Project.objects.get(name_short__exact=slug)
    # Switch to the project directory and get the file contents
    os.chdir(project.project_directory())
    directory = os.getcwd()
    contents = os.listdir(directory)

    if format == 'tar':
        import tarfile
        # Open the tar file
        filename = slug + "_backup_" + str(strftime("%Y.%m.%d.%H.%M.%S")) + ".tar.gz"
        filepath = str(os.path.join(Project.project_options.backups_directory, filename))
        tar = tarfile.open(filepath, "w:gz")
        for item in contents:
            tar.add(item)
        tar.close()
        made = 'tar'
    
    backup = ProjectBackup(parent_project=project, format=made, created=datetime.datetime.now(), file_path=filepath, file_name=filename)
    backup.save()
    
    return HttpResponseRedirect(project.get_absolute_url())

@login_required
def download_project_backup( request, slug, backup_id ):
    project = Project.objects.get( name_short__exact=slug )
    backup = ProjectBackup.objects.get( pk=backup_id )
    return HttpResponse( open( backup.file_path ) )
