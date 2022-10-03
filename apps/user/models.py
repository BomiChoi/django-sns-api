from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from apps.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('must have email')
        if not password:
            raise ValueError('must have password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=4, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
