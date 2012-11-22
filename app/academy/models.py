from django.db import models
from django.contrib.auth.models import User


class University(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('academy:detail_university', [str(self.pk)])

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    professor = models.ForeignKey(User)
    university = models.ForeignKey(University)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='CourseMembership', related_name='user_course', blank=True, null=True)

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
