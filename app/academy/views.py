from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from datetime import datetime
from django.utils.timezone import utc

from .forms import CourseForm, CourseProfessorForm
from .models import Course, CourseMembership


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
            if data.get('admin') is None:
                course.admin = request.user
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

    variables = RequestContext(request, {
        'course': course,
        'members': members,
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

    if course.admin == usr:
        raise Http404('Owner can not leave the course')
    try:
        membership = CourseMembership.objects.get(user=usr, course=course)
    except:
        raise Http404('You are not a member of this course')

    membership.delete()
    return HttpResponseRedirect(course.get_absolute_url())


@login_required
def acceptcourse(request, id, uid):
    course = get_object_or_404(Course, admin=request.user, pk=id)
    membership = get_object_or_404(CourseMembership, user_id=uid, course=course, status=2)
    membership.status = 1
    membership.save()

    return HttpResponseRedirect(course.get_absolute_url())
