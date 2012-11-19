from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext

from friendship.models import  Friend
from postman.models import Message

from .forms import StatusForm, EditProfileForm, CommentStatusForm
from .models import Profile, Status, CommentStatus

from datetime import datetime

# from forms import RegistrationForm
# from models import UserAvatar


def comment(request, id):
    if request.method == 'POST':
        form = CommentStatusForm(request.POST or None)
        if form.is_valid():
            #print 'test'
            status = Status.objects.get(id=id)
            new_comment = form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.status = status
            new_comment.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('userprofile:comment', args=(id,)))
            return HttpResponseRedirect(previous_url)
    else:
        status = get_object_or_404(Status, id=id)
        comments = CommentStatus.objects.filter(status=status)
        form = CommentStatusForm()

    variables = RequestContext(request, {
        'status': status,
        'comments': comments,
        'form': form
    })
    return render_to_response('comment.html', variables)


@login_required
def write_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = reverse('userprofile:detail', args=(request.user,))
            return HttpResponseRedirect(previous_url)
    else:
        form = StatusForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('write_status.html', variables)


def statuses(request):
    statuses = Status.objects.all()
    # paginator = Paginator(statuses_list, 2)

    # page = request.GET.get('page')
    # try:
    #     status = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     status = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     status = paginator.page(paginator.num_pages)
    variables = RequestContext(request, {
        'status': statuses
        })
    return render_to_response('statuses.html', variables)


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
    statuses = Status.objects.all()

    variables = RequestContext(request, {
        'user_profile': user,
        'friends': friends,
        'statuses': statuses,
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
