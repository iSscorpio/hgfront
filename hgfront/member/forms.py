# General Libraries
import datetime
# Django Libraries
from django.contrib.auth.models import User
import django.newforms as forms
# Project Libraries

class MemberRegisterForm(forms.Form):
    """Register a member"""
    member_username = forms.CharField(max_length=25)
    member_email = forms.EmailField()
    member_password = forms.CharField(widget=forms.PasswordInput)
    member_verify_password = forms.CharField(widget=forms.PasswordInput)
    member_real_name = forms.CharField()
    