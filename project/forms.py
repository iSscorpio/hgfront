# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
from django.newforms import ModelForm
# Project Libraries
import core.config
from project.models import Project, ProjectNews

available_styles = (
    ('default', 'Default'),
    ('gitweb', 'Gitweb'),
)

class NewProjectForm(forms.Form):
    project_id = forms.CharField(max_length=50, label="Project ID", help_text="A unique short name for your project (Max 50 Char)")
    project_name=forms.CharField(max_length=255, label="Project Name", help_text="The full name of your project (Max 255 Char)")
    short_description=forms.CharField(max_length=255, label="Project Short Description", help_text="A short description of your project (Max 255 Char)")
    full_description=forms.CharField(widget=forms.widgets.Textarea())
    project_icon=forms.ImageField(required=False)
    hgweb_style=forms.ChoiceField(choices=available_styles)
    t_and_c=forms.BooleanField(required=True, label="Terms and Conditions", help_text="You agree to the T&C's of this site.")
    
    def clean_project_id(self):
        project_id = self.cleaned_data.get('project_id', '')
        num_letters = len(project_id)
        if num_letters < 4:
            raise forms.ValidationError("A project name must be at least 4 characters long!")
        
        if Project.projects.all().filter(project_id__exact = project_id):
            raise forms.ValidationError("A project with this name already exists!")
        
        return project_id

class JoinRequestForm(forms.Form):
    username=forms.CharField(max_length=255)
    action=forms.CharField(max_length=255)
    
class ProjectNewsForm(forms.Form):
    news_title=forms.CharField(max_length=255)
    news_body=forms.CharField(widget=forms.widgets.Textarea())
    frontpage=forms.CheckboxInput()