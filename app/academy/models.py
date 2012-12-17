from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.mail import send_mail

from app.timelines.models import Timeline
from app.events.models import Event
from app.events import notification


class University(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    domain = models.CharField(max_length=50)

    members = models.ManyToManyField(User, through='UniversityMembership')

    timelines = generic.GenericRelation(Timeline)

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail', [self.slug])

    def __unicode__(self):
        return self.name

    @property
    def students(self):
        return self.members.filter(academy_roles__role=1, university=self)

    @property
    def professors(self):
        return self.members.filter(academy_roles__role=2, university=self)

    @property
    def school_admins(self):
        return self.members.filter(academy_roles__role=3, university=self)


class UniversityMembership(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'Students'),
        (2, 'Professors'),
        (3, 'School Admins,'),
    )
    user = models.ForeignKey(User, related_name='academy_roles')
    role = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    university = models.ForeignKey(University, related_name='academy_roles')
    joined_at = models.DateTimeField(blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    professor = models.ForeignKey(User)
    university = models.ForeignKey(University)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='CourseMembership', related_name='user_course', blank=True, null=True)

    timelines = generic.GenericRelation(Timeline)
    events = generic.GenericRelation(Event)

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail_course', [self.university.slug, str(self.pk)])

    def __unicode__(self):
        return self.name

    @property
    def total_students(self):
        return self.coursemembership_set.filter(status=1).count()


class CourseMembership(models.Model):
    MEMBERSHIP_STATUS = (
        (1, 'Active'),
        (2, 'Request to join'),
        (3, 'Invited'),
    )
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    status = models.IntegerField(choices=MEMBERSHIP_STATUS, default=2)
    joined_at = models.DateTimeField(blank=True, null=True)


class CourseFiles(models.Model):
    course = models.ForeignKey(Course)
    attachment = models.FileField(upload_to='course/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Syllabus(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course)
    attachment = models.FileField(upload_to='syllabus/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course)
    attachment = models.FileField(upload_to='assignment/', blank=True, default='')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail_assignment', [self.course.university.slug, str(self.course.pk), str(self.pk)])

    def __unicode__(self):
        return self.name


class AssignmentSubmit(models.Model):
    user = models.ForeignKey(User, related_name='assignments')
    assignment = models.ForeignKey(Assignment)
    attachment = models.FileField(upload_to='assignment/', blank=True, default='')
    grade = models.CharField(max_length=5)
    comment = models.TextField()

    def __unicode__(self):
        return 'Grade: %s, Professor Comment: %s' % (self.grade, self.comment)


class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


def auto_add_users_into_university(sender, instance, created, **kwargs):

    if created:
        instance.slug = slugify(instance.name)
        instance.save()

        users = User.objects.filter(email__endswith=instance.domain)

        for user in users:
            UniversityMembership.objects.create(user=user, university=instance,
                    role=1)
post_save.connect(auto_add_users_into_university, sender=University, dispatch_uid='app.academy.models.auto_add_users_into_university')


def send_email_course_invitation(sender, instance, created, **kwargs):
    if created:
        send_mail('COURSE INVITATION', settings.DEFAULT_CONTENT_EMAIL_COURSE, settings.DEFAULT_FROM_EMAIL, [instance.user.email])
    return True


post_save.connect(send_email_course_invitation, sender=CourseMembership, dispatch_uid='app.academy.models.send_email_course_invitation')


def send_email_assignment(sender, instance, created, **kwargs):
    if created:
        members = instance.course.coursemembership_set.filter(status=1)
        for member in members:
            send_mail('New Assignment Notification', settings.DEFAULT_CONTENT_EMAIL_ASSIGNMENT, settings.DEFAULT_FROM_EMAIL, [member.user.email])
            notification.notify()   # Penggunaan Celery
    return True


post_save.connect(send_email_assignment, sender=Assignment, dispatch_uid='app.academy.models.send_email_assignment')


def send_email_grade(sender, instance, created, **kwargs):
    if instance.grade:
        send_mail('New Grade Notification', settings.DEFAULT_CONTENT_EMAIL_ASSIGNMENT, settings.DEFAULT_FROM_EMAIL, [instance.user.email])
    return True


post_save.connect(send_email_grade, sender=AssignmentSubmit, dispatch_uid='app.academy.models.send_email_grade')
