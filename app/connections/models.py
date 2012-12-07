from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from friendship.models import FriendshipRequest


def notify_facebook_friends(sender, instance, created, **kwargs):
    if created:
        subject = '%s add you as a friend' % instance.from_user.username
        content = '%s add you as a friend' % instance.from_user.username
        print "#############################"
        print subject
        print content
        print instance.to_user.email
        print settings.DEFAULT_FROM_EMAIL
        print "#############################"
        send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [instance.to_user.email])
    return True

post_save.connect(notify_facebook_friends, sender=FriendshipRequest, dispatch_uid='app.connection.models.notify_facebook_friends')
