import datetime, os
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
# Project Libraries
from hgfront.member.forms import MemberRegisterForm
from hgfront.member.models import Member
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