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
    from project.models import Project, ProjectPermissionSet
    existing = ProjectPermissionSet.objects.filter(project__id = instance.id, is_default=True)
    if not existing:
        permission_set = ProjectPermissionSet(is_default=True, project=instance, user=None)
        permission_set.save()

def create_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path already exists, and if not this is a new project so creates path.
    """
    try:
        shutil.os.mkdir(instance.project_directory)
    except:
        IOError("Failed to create project directory")

def delete_project_dir(sender, instance, signal, *args, **kwargs):
    """
    Checks to see if path still exists for project and if it does, deletes it.
    """
    if bool(os.path.isdir(instance.project_directory)):
        return bool(shutil.rmtree(instance.project_directory))

def create_hgwebconfig(sender, instance, signal, *args, **kwargs):
    """
    Creates a hgweb.config file for use with hgwebdir
    """
    if bool(os.path.isdir(instance.project_directory)):
        config = open(os.path.join(instance.project_directory, 'hgweb.config'), 'w')
        config.write('[collections]\n')
        config.write('%s = %s\n\n' % (instance.project_directory, instance.project_directory))
        config.write('[web]\n')
        config.write('style = %s' % instance.hgweb_style)
        config.close()
        shutil.copy(os.path.join(settings.HGFRONT_TEMPLATES_PATH, 'project/hgwebdir.txt'), os.path.join(instance.project_directory, 'hgwebdir.cgi'))
        os.chmod(os.path.join(instance.project_directory, 'hgwebdir.cgi'), 0755)
        return True
        
def create_wikipage(sender, instance, signal, *args, **kwargs):
    from wiki.models import Page
    page, created = Page.objects.get_or_create(name="Main_Page", parent_project=instance)
    if created:
        page.content = "This is the main wiki page for this project, write something here!"
        page.save()

def send_email_to_owner(sender, instance, signal, *args, **kwargs):
	"""Send the project owner a reminder email about their project"""
	from project.models import Project
	try:
		owner = instance.project_manager
		email_intro = "This email is from " + Project.project_options.site_name +  " to advise you of the project you have created."

		email_body = render_to_string("project/email/project_created.txt",
			{
				'email_intro': email_intro,
				'project_name': instance.project_name,
				'project_short_name': instance.short_description,
				'project_desription': instance.full_description,
	        }
        )
    
		email = EmailMessage(instance.project_name + " created", email_body, 'noreply@testing.com', [owner.email])
		try:
			email.send()
		except:
			pass
	except User.DoesNotExist:
		pass
	else:
		print "Email sent to %s" % owner.email
