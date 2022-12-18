from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
# from sorl.thumbnail import delete, get_thumbnail

from core.models import BaseMedia, SlugModel, BaseModel
from users.managers import ProfileManager


class Profile(AbstractBaseUser, PermissionsMixin, BaseModel):
    objects = ProfileManager()

    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
        null=True,
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
    is_superuser = models.BooleanField(
        'админ',
        default=False,
        null=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)
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


class ProfileMedia(BaseMedia):
    profile = models.ForeignKey(
        Profile,
        verbose_name='медиа',
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'media'
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'


class ProfileContacts(SlugModel):
    profile = models.ForeignKey(
        Profile,
        verbose_name='ссылка на профиль',
        on_delete=models.CASCADE,
    )
    # service = models.ForeignKey(

    # )


class ProfileLink(SlugModel):
    profile = models.ForeignKey(
        Profile,
        verbose_name='ссылка на',
        on_delete=models.CASCADE,
    )
