from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from datetime import datetime
from django.utils.timezone import utc

from .forms import CourseForm, UniversityForm, CourseProfessorForm, SyllabusForm
from .models import Course, CourseMembership, Syllabus

from app.timelines.forms import *

import datetime


@login_required
def createuniversity(request, template='university/create.html'):
    if request.method == 'POST':
        form = UniversityForm(request.POST or None)

        if form.is_valid():
            #data = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('academy:create_university'))

    else:
        form = UniversityForm()
        #form = CourseForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render(request, template, variables)


@login_required
def createcourse(request, template='course/create.html'):
    if request.method == 'POST':
        if request.user.is_professor():
            form = CourseProfessorForm(request.POST or None)
        else:
            form = CourseForm(request.POST or None)

        if form.is_valid():
            data = form.cleaned_data
            users = data.get('members')
            course = form.save(commit=False)
            if data.get('professor') is None:
                course.professor = request.user
            course.save()
            for user in users:
                membership, new = CourseMembership.objects.get_or_create(
                    user=user, course=course)
                membership.status = 3
                membership.save()
            return HttpResponseRedirect(reverse('academy:course'))

    else:
        if request.user.is_professor():
            form = CourseProfessorForm()
        else:
            form = CourseForm()
        #form = CourseForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render(request, template, variables)


@login_required
def course(request):
    courses = Course.objects.all()
    variables = RequestContext(request, {
        'courses': courses
        })
    return render_to_response('course/index.html', variables)


@login_required
def detailcourse(request, id, template='course/detail.html'):
    course = get_object_or_404(Course, pk=id)
    members = course.coursemembership_set.all()

    timeline_list = course.timelines.all()
    paginator = Paginator(timeline_list, 10)

    page = request.GET.get('page')
    try:
        timelines = paginator.page(page)
    except PageNotAnInteger:
        timelines = paginator.page(1)
    except EmptyPage:
        timelines = paginator.page(paginator.num_pages)

    syllabus_list = Syllabus.objects.filter(course=course)
    paginator2 = Paginator(syllabus_list, 10)

    page2 = request.GET.get('page2')
    try:
        syllabuses = paginator2.page(page2)
    except PageNotAnInteger:
        syllabuses = paginator2.page(1)
    except EmptyPage:
        syllabuses = paginator2.page(paginator.num_pages)

    variables = RequestContext(request, {
        'course': course,
        'members': members,
        'timelines': timelines,
        'syllabuses': syllabuses,
    })
    return render(request, template, variables)


@login_required
def joincourse(request, id, template='course/joined.html'):
    course = get_object_or_404(Course, pk=id)

    membership, new = CourseMembership.objects.get_or_create(user=request.user,
            course=course)

    if membership.status == 1:
        raise Http404()

    elif membership.status == 3:
        membership.status = 1
        membership.joined_at = datetime.datetime.now().replace(tzinfo=utc)

    else:
        membership.status = 2

    membership.save()

    variables = RequestContext(request, {
        'membership': membership
    })
    return render(request, template, variables)


@login_required
def leavecourse(request, id, uid, template='course/joined.html'):
    course = get_object_or_404(Course, pk=id)
    usr = get_object_or_404(User, id=uid)

    if course.professor == usr:
        raise Http404('Owner can not leave the course')
    try:
        membership = CourseMembership.objects.get(user=usr, course=course)
    except:
        raise Http404('You are not a member of this course')

    membership.delete()
    return HttpResponseRedirect(course.get_absolute_url())


@login_required
def acceptcourse(request, id, uid):
    course = get_object_or_404(Course, professor=request.user, pk=id)
    membership = get_object_or_404(CourseMembership, user_id=uid, course=course, status=2)
    membership.status = 1
    membership.save()

    return HttpResponseRedirect(course.get_absolute_url())


@login_required
def update_timeline(request, id, timeline_type='text'):
    course = get_object_or_404(Course, id=id)
    user = get_object_or_404(User, is_active=True, username=request.user.username, user_course=course)

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
        form = form_class(request.POST, request.FILES, content_object=course)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = user
            t.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = form_class(content_object=course)
    variables = RequestContext(request, {
        'form': form
    })
    template = 'userprofile/upload_%s.html' % timeline_type
    return render(request, template, variables)


def syllabus(request, id):
    if request.method == 'POST':
        form = SyllabusForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            course = get_object_or_404(Course, pk=id)
            new_syllabus = form.save(commit=False)
            new_syllabus.course = course
            new_syllabus.save()
            previous_url = reverse('academy:detail_course', args=(id,))
            return HttpResponseRedirect(previous_url)
    else:
        form = SyllabusForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('course/create_syllabus.html', variables)
