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
class ProjectTestCase(TestCase):
    """ A test case for testing project related stuff """

    fixtures = ['data.json']

    def setUp(self):
        self.client.login(username='test_admin', password='test_admin')
        repo_dir_setting = Setting.objects.get(attribute_name=u'repository_directory')
        repo_backup_setting = Setting.objects.get(attribute_name=u'backups_directory')
        repo_dir_setting.value = my_repo_dir
        repo_backup_setting.value = my_backup_dir
        repo_dir_setting.save()
        repo_backup_setting.save()

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

    def setUp(self):
        super(self.__class__, self).setUp()
        self.client.logout()
