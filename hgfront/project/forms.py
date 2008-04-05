# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
from django.newforms import ModelForm
# Project Libraries
import hgfront.config
from hgfront.project.models import Project, ProjectNews

available_styles = (
    ('default', 'Default'),
    ('gitweb', 'Gitweb'),
)

class NewProjectForm(forms.Form):
    name_short = forms.CharField(max_length=50)
    name_long=forms.CharField(max_length=255)
    description_short=forms.CharField(max_length=255)
    description_long=forms.CharField(widget=forms.widgets.Textarea())
    hgweb_style=forms.ChoiceField(choices=available_styles)
    
    def clean_name_short(self):
        name_short = self.cleaned_data.get('name_short', '')
        num_letters = len(name_short)
        if num_letters < 4:
            raise forms.ValidationError("A project name must be at least 4 characters long!")
        
        if Project.projects.all().filter(name_short__exact = name_short):
            raise forms.ValidationError("A project with this name already exists!")
        
        return name_short

class JoinRequestForm(forms.Form):
    username=forms.CharField(max_length=255)
    action=forms.CharField(max_length=255)
    
class ProjectNewsForm(forms.Form):
    news_title=forms.CharField(max_length=255)
    news_body=forms.CharField(widget=forms.widgets.Textarea())
    frontpage=forms.CheckboxInput()