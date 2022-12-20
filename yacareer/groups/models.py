from django.db import models

from core.models import BaseModelImage, BaseModelMedia
from users.models import Profile


class Group(BaseModelImage):
    name = models.CharField('название', max_length=256)
    about = models.CharField('описание', max_length=1024)
    members = models.ManyToManyField(
        Profile,
        'GroupMembers',
        'members',
        'участники',
    )

    class Meta:
        default_related_name = 'groups'
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class GroupMembers(models.Model):
    user = models.ForeignKey(
        Profile,
        models.CASCADE,
        verbose_name='пользователь',
    )
    group = models.ForeignKey(Group, models.CASCADE, verbose_name='группа')
    is_staff = models.BooleanField('персонал', default=False)
    is_owner = models.BooleanField('владелец', default=False)


class GroupMedia(BaseModelMedia):
    group = models.ForeignKey(Group, models.CASCADE, verbose_name='группа')

    class Meta:
        default_related_name = 'media'
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'
