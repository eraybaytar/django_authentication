from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Kullanici',
        related_name='userprofile'
    )
    def __str__(self):
        return self.user.username

class UserToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='token'
    )
    refresh = models.TextField() #key
    access = models.TextField() #session_key
    last_activity = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username