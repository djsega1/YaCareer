from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from core.models import BaseModelImage, BaseModelMedia, BaseModelSlug
from services.models import Service


class ProfileManager(BaseUserManager):

    def is_activated(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .only('id', 'email', 'is_superuser', 'is_staff',)
        )

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

    def get_queryset(self):
        return (
            super().get_queryset()
            .prefetch_related(
                models.Prefetch(
                    'media',
                ),
                models.Prefetch(
                    'links',
                ),
            )
        )


class Profile(AbstractBaseUser, PermissionsMixin, BaseModelImage):
    objects = ProfileManager()

    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
        default='',
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
        default='',
    )
    email = models.EmailField(
        'почта',
        unique=True,
    )
    is_active = models.BooleanField(
        'активная учетная запись',
        default=True,
        null=True,
    )
    is_staff = models.BooleanField(
        'персонал',
        default=False,
        null=True,
    )
    is_superuser = models.BooleanField(
        'админ',
        default=False,
        null=True,
    )
    is_open_to_work = models.BooleanField(
        'в поисках работы',
        default=False,
        null=True,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    about = models.CharField(
        'описание',
        max_length=1024,
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        'дата рождения',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'

    class Meta:
        default_related_name = 'profiles'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class ProfileMedia(BaseModelMedia):
    profile = models.ForeignKey(
        Profile,
        verbose_name='медиа',
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'media'
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

    def __str__(self):
        return self.name


class ProfileLinks(BaseModelSlug):
    profile = models.ForeignKey(
        Profile,
        verbose_name='ссылка на профиль',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        verbose_name='сервис',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'
        default_related_name = 'links'

    def __str__(self):
        return self.slug
