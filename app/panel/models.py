from django.db import models
from django.contrib.auth.models import User


class UserAvatar(models.Model):
    User = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='userprofile/')
