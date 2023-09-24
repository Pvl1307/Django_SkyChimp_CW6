from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone_number = models.CharField(max_length=40, verbose_name='Phone number', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)

    verification_token = models.CharField(max_length=15, verbose_name='Verification code', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Verification status ')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_active', 'Can change user activity')
        ]
