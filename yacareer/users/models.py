from django.contrib.auth.models import (
    AbstractUser, UserManager as AbstractUserManager
)
from django.db import models

from survey.models import TestResult


class ProfileManager(AbstractUserManager):
    def active(self):
        queryset = self.get_queryset().filter(is_active=True)
        queryset.filter(username=None).update(username='Не указано')
        return queryset

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superusers must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusers must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)

    def published(self):
        return (
            self.get_queryset()
                .only('email')
        )


class Profile(AbstractUser):
    objects = ProfileManager()
    email = models.EmailField(unique=True, verbose_name='эл. почта')
    test_result = models.OneToOneField(TestResult, on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       verbose_name='Результат теста',
                                       help_text='Результаты теста')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f' {self.email}'
