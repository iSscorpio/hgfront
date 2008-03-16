import datetime, os
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
# Project Libraries
from hgfront.member.forms import MemberRegisterForm, MemberLoginForm
from hgfront.member.models import Member
from hgfront.project.models import Project
# Create your views here.


@transaction.commit_on_success
def member_register(request):
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            user = User.objects.create_user(
                    username = form.cleaned_data['member_username'],
                    email = form.cleaned_data['member_email'],
                    password = form.cleaned_data['member_password']
                    )
            member = Member(member_user = user, member_homepage = 'http://digitalspaghetti.me.uk')
            member.save()
            return HttpResponseRedirect(reverse('project-list'))
            
    else:
        form = MemberRegisterForm()
    return render_to_response('member/member_register.html',
        {
            'form':form
        }, context_instance=RequestContext(request)
    )
    
def member_login(request):
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['member_username']
            password = form.cleaned_data['member_password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('member-home'))
            else:
                # Show an error page
                return HttpResponseRedirect(reverse('member-login'))
    else:
        form = MemberLoginForm()
    return render_to_response('member/login.html',
        {
         'form': form
        }, context_instance=RequestContext(request)
    )
    
def member_logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('project-list'))

def member_home(request):
    user = auth.get_user(request)
    
    user_projects_owns = Project.objects.filter(user_owner = user)
    return render_to_response('member/home.html',
        {
         'user': user,
         'user_projects_owns': user_projects_owns
        }, context_instance=RequestContext(request)
    )
