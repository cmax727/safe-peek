from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save


class UserAvatar(models.Model):
    User = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='userprofile/')


def SendEmailConfirmation(sender, instance, **kwargs):
    if kwargs.get('created'):
        send_mail('Email From reg new User Socialnetwork', "wass", 'ronald.tampubolon@sixceed.com', [instance.email])

post_save.connect(SendEmailConfirmation, sender=User, dispatch_uid="uuid")
