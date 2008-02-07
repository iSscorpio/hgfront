from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Project, ProjectPermissionSet
from hgfront.config.models import Setting
from django.contrib.auth.models import User

# Put your repo and backups path here before testing until
# I find a way to get the settings from the normal database
# instead of the temporary test database that's created when
# tests are run
my_repo_dir = '/home/alisic/repos/'
my_backup_dir = my_repo_dir + 'backups/'
class HGFTestCase(TestCase):
    """A base test case class for hgfront testing. Test cases should extend this class.
    `fixtures` is a list of fixtures to be used as data. `username` and `password` are
    the username and password that are to be used when testing sites as if you were logged in.
    A User with the username and password that are provided should exist in the fixtures given.
    If anonymous is set to False, setUp will log in the client before doing any tests. If it's
    set to True, it will perform the tests as an anonymous user"""
    anonymous = False
    fixtures = ['data.json']
    username = 'test_admin'
    password = 'test_admin'
    def setUp(self):
        """
        The set up here makes the test use the repository and backup directory specified
        in the module. Once I find out how to switch databases on the fly to pull it out
        from the main database instead of the one that's created temporarily for tests,
        you won't have to specify my_repo_dir and my_backup_dir in the module.
        This set up also checks if anonymous is set to True or False and logs the user 
        in accordingly 
        """
        repo_dir_setting = Setting.objects.get(attribute_name=u'repository_directory')
        repo_backup_setting = Setting.objects.get(attribute_name=u'backups_directory')
        repo_dir_setting.value = my_repo_dir
        repo_backup_setting.value = my_backup_dir
        repo_dir_setting.save()
        repo_backup_setting.save()
        if not self.anonymous:
            self.client.login(username=self.username, password=self.password)

class ProjectTestCase(HGFTestCase):
    """ A test case for testing project related stuff """
    def test_project_list_view(self):
        response = self.client.get(reverse('project-list'))

        self.assert_(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project_list.html')
    
    def test_project_detail_view(self):
        project = Project.objects.get(name_short='manhattan')
        response = self.client.get(project.get_absolute_url())

        self.assert_(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project_detail.html')
        #using context[0] here because for some strange reason, the test
        #gets a list of 6 identical contexts. TODO: find out wtf
        self.assertEquals(response.context[0]['project'], project)

class AnonymousProjectTestCase(ProjectTestCase):
    """ This is like the ProjectTestCase test case only it does the testing
    with an anonymous user, whereas ProjectTestCase does the tests with a 
    logged in user"""
    anonymous = True
