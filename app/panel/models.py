from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    User = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='userprofile/')
