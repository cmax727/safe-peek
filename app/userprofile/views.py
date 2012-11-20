from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from friendship.models import  Friend
from postman.models import Message

from .forms import EditProfileForm, UserListForm
from .models import Profile

from app.timelines.forms import *

from datetime import datetime


@login_required
def usergroup(request, template='userprofile/usergroup.html'):
    if request.user.is_superuser:
        param = 'School Admin'
    else:
        param = 'Professor'

    list_user = User.objects.filter(groups__name=param)
    if request.method == 'POST':
        form = UserListForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(id=request.POST.get('username'))
            g = Group.objects.get(name=param)
            g.user_set.add(user)
    else:
        form = UserListForm()

    variables = RequestContext(request, {
        'form': form,
        'list_user': list_user
    })
    return render(request, template, variables)


def main(request, template='userprofile/index.html'):
    variables = RequestContext(request, {
    })
    return render(request, template, variables)


def setread(request, template='postman/base_folder.html'):
    pks = request.POST.getlist('pks', '')
    tpks = request.POST.getlist('tpks', '')
    filter = Q(pk__in=pks) | Q(pk__in=tpks)
    #idm = request.POST.getlist('tpks', '')
    #msg = Message.objects.get(id=idm)
    Message.objects.filter(filter).update(read_at=datetime.now())

    previous_url = request.META.get('HTTP_REFERER', reverse('postman_inbox'))
    return HttpResponseRedirect(previous_url)


def setunread(request, template='postman/base_folder.html'):
    pks = request.POST.getlist('pks', '')
    tpks = request.POST.getlist('tpks', '')
    filter = Q(pk__in=pks) | Q(pk__in=tpks)
    #idm = request.POST.getlist('tpks', '')
    #msg = Message.objects.get(id=idm)
    Message.objects.filter(filter).update(read_at=None)
    #update.save()
    #print idm
    #print msg.id
    previous_url = request.META.get('HTTP_REFERER', reverse('postman_inbox'))
    return HttpResponseRedirect(previous_url)


def profile_detail(request, username, template='userprofile/detail.html'):
    user = get_object_or_404(User, username=username, is_active=True)
    friends = Friend.objects.friends(user)

    variables = RequestContext(request, {
        'user_profile': user,
        'friends': friends,
    })
    return render(request, template, variables)


@login_required
def edit(request, username, template='userprofile/edit.html'):
    user = get_object_or_404(User, is_active=True, username=username)
    user_profile, created = Profile.objects.get_or_create(user=user)

    if request.user != user:
        raise Http404('You are not allowed to edit this page')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # use existing profile instead of creating one
            profile = form.save()

            profile.user.username = cleaned_data.get('username')
            profile.user.first_name = cleaned_data.get('first_name')
            profile.user.last_name = cleaned_data.get('last_name')
            profile.user.save()
            return HttpResponseRedirect(reverse('userprofile:detail', args=[profile.user.username]))

    else:
        initial_data = {
            'user': user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        form = EditProfileForm(initial=initial_data, instance=user_profile)

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)


@login_required
def user_groups(request, username, template='userprofile/groups.html'):
    user = get_object_or_404(User, is_active=True, username=username)

    variables = RequestContext(request, {
        'user': user,
        'memberships': user.groupmembership_set.all().prefetch_related('user', 'group')
    })
    return render(request, template, variables)


@login_required
def update_timeline(request, timeline_type='text'):
    user = get_object_or_404(User, is_active=True, username=request.user.username)
    form_class = None

    if timeline_type == 'text':
        form_class = TextTimelineForm
    elif timeline_type == 'picture':
        form_class = ImageTimelineForm
    elif timeline_type == 'youtube':
        form_class = YoutubeTimelineForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, content_object=user.profile)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = user
            t.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = form_class(content_object=user.profile)
    variables = RequestContext(request, {
        'form': form
    })
    template = 'userprofile/upload_%s.html' % timeline_type
    return render(request, template, variables)
