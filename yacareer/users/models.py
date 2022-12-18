from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
# from sorl.thumbnail import delete, get_thumbnail

from users.managers import ProfileManager


class Profile(AbstractBaseUser, PermissionsMixin):
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
    avatar = models.ImageField(
        'аватар',
        default='static_dev/img/user.png',
    )

    USERNAME_FIELD = 'email'

    class Meta:
        default_related_name = 'profiles'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
