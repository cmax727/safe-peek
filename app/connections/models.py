from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Group(models.Model):
    PRIVACY_CHOICES = (
        (1, 'Open'),
        (2, 'Invite'),
    )
    name = models.CharField(max_length=80)
    description = models.TextField()
    privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=1)
    created_by = models.ForeignKey(User)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.name
