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
    user = 'test_admin'
    passwords = {
        'test_admin':'test_admin',
        'charles':'charles',
        'johnny':'johnny',
    }
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
            self.client.login(username=self.user, password=self.passwords[self.user])

class ProjectTestCase(HGFTestCase):
    """ A test case for testing project related stuff """
    def test_project_list_view(self):
        """ Tests the project list view """
        expected = {
            'status_code':200,
            'template_used':'project/project_list.html',
        }
        response = self.client.get(reverse('project-list'))
        self.assert_(response.status_code == expected['status_code'])
        self.assertTemplateUsed(response, expected['template_used'])
    
    def test_project_detail_view(self):
        expected = {
            'project':Project.objects.get(name_short='manhattan'),
            'status_code':200,
            'template_used':'project/project_detail.html'
        }
        response = self.client.get(expected['project'].get_absolute_url())
        self.assert_(response.status_code == expected['status_code'])
        self.assertTemplateUsed(response, expected['template_used'])
        #using context[0] here because for some strange reason, the test
        #gets a list of 6 identical contexts. TODO: find out wtf
        self.assertEquals(response.context[0]['project'], expected['project'])

class AnonymousProjectTestCase(ProjectTestCase):
    """ This is like the ProjectTestCase test case only it does the testingd
    with an anonymous user, whereas ProjectTestCase does the tests with a 
    logged in user"""
    anonymous = True

class SecretProjectTestCase(HGFTestCase):
    """ This tests stuff against the project that has minimal permissions enabled """
    project_used = Project.objects.get(name_short='secret_project')

    def test_unauthorized_403(self):
        """ An unauthorized but logged in user should get a 403 error """
        expected = {
            'status_code':403,
            'template_used':'403.html',
        }
        response = self.client.get(self.project_used.get_absolute_url())
        self.assert_(response.status_code == expected['status_code'])
        self.assertTemplateUsed(response, expected['template_used'])

    def test_anonymouse_403(self):
        """ An anonymous user should get a 403 error """
        expected = {
            'status_code':403,
            'template_used':'403.html',
        }
        self.client.logout()
        response = self.client.get(self.project_used.get_absolute_url())
        self.client.login(username=self.user, password=self.passwords[self.user])
        self.assert_(response.status_code == expected['status_code'])
        self.assertTemplateUsed(response, expected['template_used'])
    
    def test_authorized_200(self):
        """ An authorized user should get a 200 response code """
        expected = {'status_code':200,}
        authorized_username = 'charles'
        self.client.login(username=authorized_username, password=self.passwords[authorized_username])
        response = self.client.get(self.project_used.get_absolute_url())
        self.assert_(response.status_code == expected['status_code'])
        self.client.login(username=self.user, password=self.passwords[self.user])
    
    def test_admin_200(self):
        """ The admin should be able to view the project and get a 200 response code """
        expected = {'status_code':200,}
        authorized_username = 'johnny'
        self.client.login(username=authorized_username, password=self.passwords[authorized_username])
        response = self.client.get(self.project_used.get_absolute_url())
        self.assert_(response.status_code == expected['status_code'])
        self.client.login(username=self.user, password=self.passwords[self.user])
