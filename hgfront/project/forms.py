# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
# Project Libraries
from hgfront.config.models import InstalledStyles
from hgfront.project.models import Project

class NewProjectForm(forms.Form):
    name_short = forms.CharField(max_length=50)
    
class NewProjectStep2(forms.Form):
    name_short=forms.CharField(max_length=50)
    name_long=forms.CharField(max_length=255)
    description_short=forms.CharField(max_length=255)
    description_long=forms.CharField(widget=forms.widgets.Textarea())
    # Need to get the current logged in users name
    user_owner=forms.CharField()#widget=forms.widgets.HiddenInput())
    pub_date=forms.DateTimeField()
    # Need to make this take the values from the db
    hgweb_style=forms.MultipleChoiceField([('default','Default'),('gitweb', 'Gitweb')])



#class ProjectCreateForm(ModelForm):
#    """
#    This form allows a registered user to create a project in the system.
#    When a project is created, it also creates a directory to store the data in.
#    """
#    class Meta:
#        model = Project
