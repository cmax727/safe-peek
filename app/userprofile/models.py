from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
## Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user = models.OneToOneField(User)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


def get_display_name(self):
    if not self.get_full_name():
        return self.username
    return self.get_full_name()
User.add_to_class('display_name', get_display_name)


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
