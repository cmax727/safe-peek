from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from friendship.models import Friend
from postman.models import Message

from .forms import EditProfileForm, UserListForm, PersonalEventForm, InterestForm, HobbyForm
from .models import Profile, Interest, Hobby

from app.academy.models import Course
from app.timelines.forms import *
from app.events.models import Event

from datetime import datetime


def main(request, template='userprofile/index.html'):

    if request.user.is_authenticated():
        return HttpResponseRedirect(request.user.get_absolute_url())
    variables = RequestContext(request, {
    })
    return render(request, template, variables)


@login_required
def my_grades(request, template='userprofile/grades.html'):
    assignments = request.user.assignments.order_by('assignment__course')
    variables = RequestContext(request, {
        'assignments': assignments
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
    Message.objects.filter(filter).update(read_at=None)
    previous_url = request.META.get('HTTP_REFERER', reverse('postman_inbox'))
    return HttpResponseRedirect(previous_url)


def profile_detail(request, username, template='userprofile/detail.html'):
    user = get_object_or_404(User, username=username, is_active=True)
    friends = Friend.objects.friends(user)
    groups = user.user_groups.all()
    courses = Course.objects.filter(Q(coursemembership__user=user) | Q(professor=user))
    timeline_list = user.profile.timelines.all()
    events = user.profile.events.all()

    for group in groups:
        events = events | group.events.all()
        timeline_list = timeline_list | group.timelines.filter(created_by=user)

    for course in courses:
        events = events | course.events.all()
        timeline_list = timeline_list | course.timelines.filter(created_by=user)

    events = events.order_by('event_date')
    timeline_list = timeline_list.order_by('-created_at')

    paginator = Paginator(timeline_list, 10)
    page = request.GET.get('page')

    try:
        timelines = paginator.page(page)
    except PageNotAnInteger:
        timelines = paginator.page(1)
    except EmptyPage:
        timelines = paginator.page(paginator.num_pages)

    variables = RequestContext(request, {
        'user_profile': user,
        'friends': friends,
        'timelines': timelines,
        'events': events,
        'text_form': TextTimelineForm(user=user),
        'image_form': ImageTimelineForm(user=user),
        'youtube_form': YoutubeTimelineForm(user=user),
        'file_form': FileTimelineForm(user=user),
    })
    return render(request, template, variables)


@login_required
def personal_event(request, template='userprofile/create_events.html'):

    if request.method == 'POST':
        form = PersonalEventForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            previous_url = reverse('userprofile:detail', args=(request.user,))
            return HttpResponseRedirect(previous_url)
    else:
        ctype = ContentType.objects.get_for_model(request.user.profile)
        event = '%s_%s' % (ctype.pk, request.user.profile.pk)
        form = PersonalEventForm(user=request.user, initial={'event': event})

    variables = RequestContext(request, {
        'form': form,
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
            profile.user.location = cleaned_data.get('location')
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

    if timeline_type == 'picture':
        form_class = ImageTimelineForm
    elif timeline_type == 'youtube':
        form_class = YoutubeTimelineForm
    elif timeline_type == 'file':
        form_class = FileTimelineForm
    else:
        form_class = TextTimelineForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, user=user)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = user
            t.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = form_class(user=user)
    variables = RequestContext(request, {
        'form': form
    })
    template = 'userprofile/upload_%s.html' % timeline_type
    return render(request, template, variables)

@csrf_exempt
def new_interest(request, username):
    if username == request.user.username:
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save()
            print interest
            request.user.profile.interests.add(interest)
            return HttpResponse('{"text": "'+interest.title+'"}')
        return HttpResponse('{"error": "Errors in fields '+str(form.errors)+'"}')

@csrf_exempt
def new_hobby(request, username):
    if username == request.user.username:
        form = HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save()
            request.user.profile.hobbies.add(hobby)
            return HttpResponse('{"text": "'+hobby.title+'"}')
        return HttpResponse('{"error": "Errors in fields '+str(form.errors)+'"}')


