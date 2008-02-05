from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Project, ProjectPermissionSet
from django.contrib.auth.models import User

class ProjectTestCase(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        pass

    def test_project_list_view(self):
        response = self.client.get(reverse('project-list'))
        self.assert_(response.status_code, 200)
    
    def test_project_detail_view(self):
        project = Project.objects.get(name_short='manhattan')
        response = self.client.get(project.get_absolute_url())
        self.assert_(response.status_code, 200)
