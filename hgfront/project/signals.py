# General Libraries
import datetime, sys, os, shutil
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.template.loader import render_to_string
# Project Libraries

def create_default_permission_set(sender, instance, signal, *args, **kwargs):
    """
    Executed on creation of a project, this defines the default permissions
    """
    from hgfront.project.models import Project, ProjectPermissionSet
    existing = ProjectPermissionSet.objects.filter(project__id = instance.id, is_default=True)
    if not existing:
        permission_set = ProjectPermissionSet(is_default=True, project=instance, user=None)
        permission_set.save()

def create_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path already exists, and if not this is a new project so creates path.
    """
    from hgfront.project.models import Project
    directory = os.path.join(Project.project_options.repository_directory, instance.name_short)
    try:
        shutil.os.mkdir(directory)
    except:
        IOError("Failed to create project directory")

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path still exists for project and if it does, deletes it.
    """
    from hgfront.project.models import Project
    directory = os.path.join(Project.project_options.repository_directory, instance.name_short)
    if bool(os.path.isdir(directory)):
        return bool(shutil.rmtree(directory))

def create_hgwebconfig(sender, instance, signal, *args, **kwargs):
    """
    Creates a hgweb.config file for use with hgwebdir
    """
    from hgfront.project.models import Project
    directory = os.path.join(Project.project_options.repository_directory, instance.name_short)
    
    if bool(os.path.isdir(directory)):
        config = open(os.path.join(directory, 'hgweb.config'), 'w')
        config.write('[collections]\n')
        config.write('%s = %s\n\n' % (directory, directory))
        config.write('[web]\n')
        config.write('style = %s' % instance.hgweb_style)
        config.close()
        shutil.copy(os.path.join(settings.HGFRONT_TEMPLATES_PATH, 'project/hgwebdir.txt'), os.path.join(directory, 'hgwebdir.cgi'))
        os.chmod(os.path.join(directory, 'hgwebdir.cgi'), 0755)
        return True
        
def create_wikipage(sender, instance, signal, *args, **kwargs):
    from hgfront.wiki.models import Page
    page, created = Page.objects.get_or_create(name="Main_Page", parent_project=instance)
    if created:
        page.content = "This is the main wiki page for this project, write something here!"
        page.save()

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
	"""Send the project owner a reminder email about their project"""
	from hgfront.project.models import Project
	try:
		owner = instance.user_owner
		email_intro = "This email is from hgfront to advise you of the project you have created."

		email_body = render_to_string("project/email/project_created.txt",
			{
				'email_intro': email_intro,
				'project_name': instance.name_long,
				'project_short_name': instance.name_short,
				'project_desription': instance.description_short
	        }
        )
    
		email = EmailMessage(instance.name_long, email_body, 'noreply@testing.com', [owner.email])
		try:
			email.send()
		except:
			pass
	except User.DoesNotExist:
		pass
	else:
		print "Email sent to %s" % owner.email
