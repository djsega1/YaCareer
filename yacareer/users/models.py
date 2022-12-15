from django.contrib.auth.models import (
    AbstractUser, UserManager as AbstractUserManager
)
from django.db import models


class ProfileManager(AbstractUserManager):
    def active(self):
        queryset = self.get_queryset().filter(is_active=True)
        queryset.filter(username=None).update(username='Не указано')
        return queryset


class Profile(AbstractUser):
    objects = ProfileManager()
    email = models.EmailField(unique=True, verbose_name='эл. почта')
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f' {self.email}'
