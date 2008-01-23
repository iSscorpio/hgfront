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
    hgweb_style=forms.MultipleChoiceField([(style.short_name, style.long_name) for style in InstalledStyles.objects.filter(is_active=True)])


class JoinRequestForm(forms.Form):
    username=forms.CharField(max_length=255)
    action=forms.CharField(max_length=255)


#class ProjectCreateForm(ModelForm):
#    """
#    This form allows a registered user to create a project in the system.
#    When a project is created, it also creates a directory to store the data in.
#    """
#    class Meta:
#        model = Project
