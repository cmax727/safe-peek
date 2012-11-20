from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from datetime import datetime
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
