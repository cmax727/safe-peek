from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from app.timelines.models import Timeline
from app.academy.models import University, UniversityMembership, Course
from allauth.account.signals import email_confirmed, user_signed_up
from allauth.socialaccount.models import SocialToken

from facepy import GraphAPI


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    USER_TYPE_CHOICES = (
        (1, 'Students'),
        (2, 'Professors'),
        (3, 'School Admins,'),
    )
    user = models.OneToOneField(User)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)

    thumbnail_picture = ImageSpecField([ResizeToFill(100, 100)],
            image_field='picture',
            format='JPEG',
            options={'quality': 90})
    small_picture = ImageSpecField([ResizeToFill(25, 25)],
            image_field='picture',
            format='JPEG',
            options={'quality': 90})

    timelines = generic.GenericRelation(Timeline)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_thumbnail_picture(self):
        res = '%simages/profile-default.jpg' % settings.STATIC_URL

        try:
            res = self.thumbnail_picture.url
        except:
            pass
        return res

    def get_small_picture(self):
        res = '%simages/profile-default.jpg' % settings.STATIC_URL

        try:
            res = self.small_picture.url
        except:
            pass
        return res


def get_display_name(self):
    if not self.get_full_name():
        return self.username
    return self.get_full_name()
User.add_to_class('display_name', get_display_name)


def is_school_admin(self):
    return self.academy_roles.filter(role=3).exists()
User.add_to_class('is_school_admin', is_school_admin)


def is_professor(self):
    return self.academy_roles.filter(role=2).exists()
User.add_to_class('is_professor', is_professor)


def active_groups(self):
    res = []

    for membership in self.groupmembership_set.prefetch_related('group').filter(status=1):
        res.append(membership.group)
    return res
User.add_to_class('active_groups', active_groups)


def active_courses(self):
    res = list(Course.objects.filter(professor=self))

    for membership in self.coursemembership_set.prefetch_related('course').filter(status=1):
        res.append(membership.course)
    return res
User.add_to_class('active_courses', active_courses)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Status(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='detail/', blank=True, default='')
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(200, 200)], image_field='image', format='JPEG',
        options={'quality': 90})
    attachment = models.FileField(upload_to='detail/', blank=True, default='')
    url_link = models.URLField(max_length=200)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class CommentStatus(models.Model):
    status = models.ForeignKey(Status)
    comment = models.TextField()
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment


@receiver(email_confirmed)
def setup_universities_upon_registration(email_address, **kwargs):
    user = email_address.user
    email = email_address.email
    username, dom = email.split('@')

    try:
        univ = University.objects.get(domain=dom)
        UniversityMembership.objects.create(university=univ, user=user)
    except:
        univ = University.objects.create(name=dom, description='new university',
                domain=dom)


@receiver(user_signed_up)
def notify_facebook_friends(request, user, **kwargs):
    try:
        user_token = SocialToken.objects.get(app__provider='facebook', account__user=user)
    except:
        return False
    graph = GraphAPI(user_token.token)
    fb_friends = graph.get('me/friends')
    fb_friends_list = []

    for friend in fb_friends['data']:
        fb_friends_list.append(friend['id'])
    users = User.objects.filter(socialaccount__uid__in=fb_friends_list,
            socialaccount__provider='facebook')

    email_content = '<p><a href="%s">%s</a> just joined social network</p>' % (user.get_absolute_url, user.display_name)
    for user in users:
        send_mail('Your friend just joined School network', email_content,
                settings.DEFAULT_FROM_EMAIL, [user.email])
    return True
