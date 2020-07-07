import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def profile_image_save_path(instance, fileName):
    extension = fileName.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('profile_image/', filename)


def introduction_image_save_path(instance, fileName):
    extension = fileName.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('introduction_image/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(email, password, username)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'ユーザ'
    name = models.CharField(max_length=255)
    username = models.CharField(
        max_length=150, unique=True, default=None, verbose_name='ユーザ名')
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='メールアドレス',)
    password = models.CharField(max_length=128, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    introduction = models.TextField(blank=True, null=True, default="")
    profile_image = models.ImageField(
        null=True, upload_to=profile_image_save_path, default="")
    background_image = models.ImageField(
        null=True, upload_to=introduction_image_save_path, default="")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )


class Relation(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='target'
    )
