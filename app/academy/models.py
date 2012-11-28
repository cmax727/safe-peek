from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save

from app.timelines.models import Timeline


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
    objects = University()

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail_course', [str(self.pk)])

    def __unicode__(self):
        return self.name


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
    members = models.ManyToManyField(User, through='AssignmentMembership')

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail_assignment', [str(self.pk)])

    def __unicode__(self):
        return self.name


class AssignmentMembership(models.Model):
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    attachment = models.FileField(upload_to='assignment/', blank=True, default='')
    grade = models.CharField(max_length=5)


def auto_add_users_into_university(sender, instance, created, **kwargs):

    if created:
        users = User.objects.filter(email__endswith=instance.domain)

        for user in users:
            UniversityMembership.objects.create(user=user, university=instance,
                    role=1)
post_save.connect(auto_add_users_into_university, sender=University, dispatch_uid='app.academy.models.auto_add_users_into_university')
