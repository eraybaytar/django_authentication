from django.db import models
from django.utils import timezone
import bcrypt
import random
import string

# Create your models here.

class User(models.Model):
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, null=True, blank=True)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(raw_password.encode(), salt).decode()

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password_hash.encode())

    def generate_token(self, field):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        setattr(self, field, token)
        self.save()
        return token

    def __str__(self):
        return self.email
