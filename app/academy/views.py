from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from datetime import datetime
from django.utils.timezone import utc

from .forms import (CourseForm, CourseFilesForm, UniversityForm, CourseProfessorForm,
        SyllabusForm, UniversityAdminForm, UniversityProfessorForm,
        UniversityCourseForm, AssignmentForm, SubmitAssignmentForm,
        SubmitAssignmentUserForm, TextTimelineForm, EventForm, StudyGroupForm)

from .forms import AcademyEventForm, AcademyTextTimelineForm, AcademyImageTimelineForm, AcademyYoutubeTimelineForm, AcademyFileTimelineForm
from .models import Course, CourseMembership, CourseFiles, Syllabus, University, Assignment, AssignmentSubmit, Event, StudyGroup
from .decorators import school_members_only
from .templatetags.university_tags import *


@login_required
def index(request, template='university/index.html'):
    universities_list = University.objects.order_by('name')
    paginator = Paginator(universities_list, 10)
    page = request.GET.get('page')

    try:
        universities = paginator.page(page)
    except PageNotAnInteger:
        universities = paginator.page(1)
    except EmptyPage:
        universities = paginator.page(paginator.num_pages)
    variables = RequestContext(request, {
        'universities': universities
    })
    return render(request, template, variables)


@login_required
def detail(request, slug, template='university/detail.html'):
    university = get_object_or_404(University, slug=slug)
    students = university.students.all()

    timeline_list = university.timelines.all()
    paginator = Paginator(timeline_list, 10)

    page = request.GET.get('page')
    try:
        timelines = paginator.page(page)
    except PageNotAnInteger:
        timelines = paginator.page(1)
    except EmptyPage:
        timelines = paginator.page(paginator.num_pages)

    ctype = ContentType.objects.get_for_model(university)
    timeline = '%s_%s' % (ctype.pk, university.pk)
    text_form = AcademyTextTimelineForm(user=request.user, initial={'timeline': timeline})
    image_form = AcademyImageTimelineForm(user=request.user, initial={'timeline': timeline})
    youtube_form = AcademyYoutubeTimelineForm(user=request.user, initial={'timeline': timeline})
    file_form = AcademyFileTimelineForm(user=request.user, initial={'timeline': timeline})

    variables = RequestContext(request, {
        'university': university,
        'students': students,
        'timelines': timelines,
        'text_form': text_form,
        'image_form': image_form,
        'youtube_form': youtube_form,
        'file_form': file_form,
    })
    return render(request, template, variables)


@login_required
def createuniversity(request, template='university/create.html'):

    if request.method == 'POST':
        form = UniversityForm(request.POST or None)

        if form.is_valid():
            #data = form.cleaned_data
            university = form.save()
            return HttpResponseRedirect(reverse('academy:detail', args=[university.slug]))

    else:
        form = UniversityForm()
        #form = CourseForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def university_admins(request, slug, template='university/choose_users.html'):

    if not request.user.is_superuser:
        raise Http404
    university = get_object_or_404(University, slug=slug)

    if request.method == 'POST':
        form = UniversityAdminForm(request.POST, university=university)

        if form.is_valid():
            admin_pks = form.cleaned_data.get('admins')
            university.academy_roles.filter(user__pk__in=admin_pks)\
                    .update(role=3)
            return HttpResponseRedirect(university.get_absolute_url())
    else:
        form = UniversityAdminForm(university=university)

    variables = RequestContext(request, {
        'form': form,
        'university': university,
        'title': 'Assign %s admins' % university
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def university_professors(request, slug, template='university/choose_users.html'):
    university = get_object_or_404(University, slug=slug)

    if request.method == 'POST':
        form = UniversityProfessorForm(request.POST, university=university)

        if form.is_valid():
            admin_pks = form.cleaned_data.get('professors')
            university.academy_roles.filter(user__pk__in=admin_pks)\
                    .update(role=2)
            return HttpResponseRedirect(university.get_absolute_url())
    else:
        form = UniversityProfessorForm(university=university)

    variables = RequestContext(request, {
        'form': form,
        'university': university,
        'title': 'Assign %s professors' % university
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def university_create_course(request, slug, template='university/create_course.html'):
    university = get_object_or_404(University, slug=slug)

    if request.method == 'POST':
        form = UniversityCourseForm(request.POST, university=university)

        if form.is_valid():
            obj = form.save()
            students = form.cleaned_data.get('students')
            for student in students:
                if student not in obj.members.all():
                    CourseMembership.objects.create(user=student,
                            course=obj, status=3)
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form = UniversityCourseForm(university=university,
                initial={'professor': request.user})

    variables = RequestContext(request, {
        'form': form,
        'university': university,
        'title': 'Create a course for %s' % university
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def course(request, slug):
    courses = Course.objects.all()
    variables = RequestContext(request, {
        'courses': courses
        })
    return render_to_response('course/index.html', variables)


@login_required
def detailcourse(request, slug, id, template='course/detail.html'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)
    members = course.coursemembership_set.all()
    assignments = course.assignment_set.all()
    files = course.coursefiles_set.all()
    study_groups = course.studygroup_set.all()
    events = course.events.order_by('event_date')

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

    ctype = ContentType.objects.get_for_model(course)
    timeline = '%s_%s' % (ctype.pk, course.pk)
    text_form = AcademyTextTimelineForm(user=request.user, initial={'timeline': timeline})
    image_form = AcademyImageTimelineForm(user=request.user, initial={'timeline': timeline})
    youtube_form = AcademyYoutubeTimelineForm(user=request.user, initial={'timeline': timeline})
    file_form = AcademyFileTimelineForm(user=request.user, initial={'timeline': timeline})

    variables = RequestContext(request, {
        'course': course,
        'members': members,
        'timelines': timelines,
        'syllabuses': syllabuses,
        'assignments': assignments,
        'files': files,
        'events': events,
        'study_groups': study_groups,
        'text_form': text_form,
        'image_form': image_form,
        'youtube_form': youtube_form,
        'file_form': file_form
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def joincourse(request, slug, id, template='course/joined.html'):
    course = get_object_or_404(Course, pk=id)

    membership, new = CourseMembership.objects.get_or_create(user=request.user,
            course=course)

    if membership.status == 1:
        raise Http404()

    elif membership.status == 3:
        membership.status = 1
        membership.joined_at = datetime.now().replace(tzinfo=utc)

    else:
        membership.status = 2

    membership.save()

    variables = RequestContext(request, {
        'membership': membership
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def leavecourse(request, slug, id, uid, template='course/joined.html'):
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


@school_members_only('slug')
@login_required
def acceptcourse(request, slug, id, uid):
    course = get_object_or_404(Course, professor=request.user, pk=id)
    membership = get_object_or_404(CourseMembership, user_id=uid, course=course, status=2)
    membership.status = 1
    membership.save()

    return HttpResponseRedirect(course.get_absolute_url())


@school_members_only('slug')
@login_required
def write_timeline(request, slug, timeline_type='text'):
    university = get_object_or_404(University, slug=slug)

    form_class = None

    if timeline_type == 'picture':
        form_class = AcademyImageTimelineForm
    elif timeline_type == 'youtube':
        form_class = AcademyYoutubeTimelineForm
    elif timeline_type == 'file':
        form_class = AcademyFileTimelineForm
    else:
        form_class = AcademyTextTimelineForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            return HttpResponseRedirect(university.get_absolute_url())
    else:
        ctype = ContentType.objects.get_for_model(university)
        timeline = '%s_%s' % (ctype.pk, university.pk)
        form = form_class(user=request.user, initial={'timeline': timeline})
    variables = RequestContext(request, {
        'form': form
    })
    template = 'university/upload_%s.html' % timeline_type
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def write_timeline_course(request, slug, id, timeline_type='text'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)

    form_class = None

    if timeline_type == 'picture':
        form_class = AcademyImageTimelineForm
    elif timeline_type == 'youtube':
        form_class = AcademyYoutubeTimelineForm
    elif timeline_type == 'file':
        form_class = AcademyFileTimelineForm
    else:
        form_class = AcademyTextTimelineForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        ctype = ContentType.objects.get_for_model(course)
        timeline = '%s_%s' % (ctype.pk, course.pk)
        form = form_class(user=request.user, initial={'timeline': timeline})
    variables = RequestContext(request, {
        'form': form
    })
    template = 'university/upload_%s.html' % timeline_type
    return render(request, template, variables)


@school_members_only('slug')
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


@school_members_only('slug')
@login_required
def syllabus(request, slug, id, template='course/create_syllabus.html'):
    if request.method == 'POST':
        form = SyllabusForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            course = get_object_or_404(Course, university__slug=slug, pk=id)
            new_syllabus = form.save(commit=False)
            new_syllabus.course = course
            new_syllabus.save()
            previous_url = reverse('academy:detail_course', args=(slug, id,))
            return HttpResponseRedirect(previous_url)
    else:
        form = SyllabusForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('course/create_syllabus.html', variables)
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def createassignment(request, slug, id, template='course/create_assignment.html'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        form = AssignmentForm(initial={'course': course})

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def report_assignment(request, slug, id, template='course/report_assignment.html'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)
    assignment = Assignment.objects.filter(course=course)

    if request.method == 'POST':
        pk = request.POST.get('assignment', '')
        if pk != '-':
            assignment = Assignment.objects.filter(course=course, pk=pk)

        if request.user == course.professor:
            uid = request.POST.get('member', '')
            if uid != '-':
                results = AssignmentSubmit.objects.filter(assignment__in=assignment, user__pk=uid)
            else:
                results = AssignmentSubmit.objects.filter(assignment__in=assignment)
        else:
            results = AssignmentSubmit.objects.filter(user=request.user, assignment__in=assignment)
    else:
        if request.user == course.professor:
            results = AssignmentSubmit.objects.filter(assignment__in=assignment)
        else:
            results = AssignmentSubmit.objects.filter(user=request.user, assignment__in=assignment)
    variables = RequestContext(request, {
        'course': course,
        'results': results
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def files(request, slug, id, template='course/upload.html'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)

    if request.method == 'POST':
        form = CourseFilesForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        form = CourseFilesForm(initial={'course': course})

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def create_study_group(request, slug, id, template='course/create_study_group.html'):
    course = get_object_or_404(Course, university__slug=slug, pk=id)

    if request.method == 'POST':
        form = StudyGroupForm(request.POST)

        if form.is_valid():
            new_study_group = form.save(commit=False)
            new_study_group.created_by = request.user
            new_study_group.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        form = StudyGroupForm(initial={'course': course, 'created_by': request.user})

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def event(request, slug, id, template='course/create_event.html'):
    #university = get_object_or_404(University, id=id)
    course = get_object_or_404(Course, university__slug=slug, pk=id)

    if request.method == 'POST':
        form = AcademyEventForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        ctype = ContentType.objects.get_for_model(course)
        event = '%s_%s' % (ctype.pk, course.pk)
        form = AcademyEventForm(user=request.user, initial={'event': event})

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def detailassignment(request, slug, aid, id, template='course/detailassignment.html'):
    assignment = get_object_or_404(Assignment, pk=id, course__pk=aid, course__university__slug=slug)
    members = assignment.course.coursemembership_set.all()

    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_submit = form.save(commit=False)
            new_submit.assignment = assignment
            new_submit.user = request.user
            new_submit.save()
            print new_submit
    else:
        form = SubmitAssignmentForm()

    variables = RequestContext(request, {
        'assignment': assignment,
        'members': members,
        'form': form
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def detail_study_group(request, slug, sid, id, template='course/detail_study_group.html'):
    assignment = get_object_or_404(Assignment, pk=id, course__pk=sid, course__university__slug=slug)
    members = assignment.course.coursemembership_set.all()

    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_submit = form.save(commit=False)
            new_submit.assignment = assignment
            new_submit.user = request.user
            new_submit.save()
            print new_submit
    else:
        form = SubmitAssignmentForm()

    variables = RequestContext(request, {
        'assignment': assignment,
        'members': members,
        'form': form
    })
    return render(request, template, variables)


@school_members_only('slug')
@login_required
def detail_assignment_user(request, slug, aid, id, uname, template='course/detailassignmentuser.html'):
    assignment = get_object_or_404(Assignment, pk=id)
    user = get_object_or_404(User, username=uname)

    if request.method == 'POST':
        ids = assignment.assignmentsubmit_set.get(user=user).id
        grade = request.POST.get('grade', '')
        comment = request.POST.get('comment', '')
        AssignmentSubmit.objects.filter(pk=ids).update(grade=grade, comment=comment)
        send_mail('New Grade Notification', settings.DEFAULT_CONTENT_EMAIL_GRADE, settings.DEFAULT_FROM_EMAIL, [user.email])
        return HttpResponseRedirect(assignment.get_absolute_url())

    submit = assignment.assignmentsubmit_set.get(user=user)
    form = SubmitAssignmentUserForm(instance=submit)
    variables = RequestContext(request, {
        'assignment': assignment,
        'submit': submit,
        'form': form
    })
    return render(request, template, variables)
