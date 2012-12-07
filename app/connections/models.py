from django.conf import settings
#from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save

from friendship.models import Friend


def send_email_friend_request(sender, instance, created, **kwargs):
    if created:
        print kwargs

        send_mail('Friend Request Notification', settings.DEFAULT_CONTENT_EMAIL_GROUP, settings.DEFAULT_FROM_EMAIL, [instance.to_user.email])
    return True

post_save.connect(send_email_friend_request, sender=Friend, dispatch_uid='friendship.models.send_email_friend_request')
