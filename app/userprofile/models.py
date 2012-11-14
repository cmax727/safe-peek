from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


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
