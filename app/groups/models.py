from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from app.timelines.models import Timeline


class GroupManager(models.Manager):
    def open_groups(self):
        qs = super(GroupManager, self).get_query_set()
        return qs.filter(privacy=1)


class Group(models.Model):
    PRIVACY_CHOICES = (
        (1, 'Open'),
        (2, 'Invite'),
    )
    name = models.CharField(max_length=80)
    description = models.TextField()
    privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=1)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='GroupMembership', related_name='user_groups', blank=True, null=True)

    timelines = generic.GenericRelation(Timeline)
    objects = GroupManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('groups:detail', [str(self.pk)])

    def get_authorize(self, **kwargs):
        tmpBool = False
        members = GroupMembership.objects.filter(status__in=[1, 2])
        if kwargs['user'] in members:
            tmpBool = True
        if self.created_by == kwargs['user']:
            tmpBool = True
        if self.privacy == 1:
            tmpBool = True
        return tmpBool


class GroupMembership(models.Model):
    MEMBERSHIP_STATUS = (
        (1, 'Active'),
        (2, 'Request to join'),
        (3, 'Invited'),
    )
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    status = models.IntegerField(choices=MEMBERSHIP_STATUS, default=2)
    joined_at = models.DateTimeField(blank=True, null=True)


class GroupStatus(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='statuses/', blank=True, default='')
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(200, 200)], image_field='image', format='JPEG',
        options={'quality': 90})
    attachment = models.FileField(upload_to='statuses/', blank=True, default='')
    url_link = models.URLField(max_length=200)
    created_by = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class GroupCommentStatus(models.Model):
    status = models.ForeignKey(GroupStatus)
    comment = models.TextField()
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment
