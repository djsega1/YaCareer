from django.db import models

from core.models import BaseModelImage, BaseModelMedia
from users.models import User


class Group(BaseModelImage):
    name = models.CharField(
        'название',
        max_length=256,
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='owner',
        verbose_name='владелец',
    )
    about = models.CharField(
        'описание',
        max_length=1024,
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(
        User,
        through='GroupMembers',
        related_name='members',
        verbose_name='группа',
    )

    class Meta:
        default_related_name = 'groups'
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self):
        return self.name


class GroupMembers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа',
    )
    is_staff = models.BooleanField('персонал', default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'group'),
                name='rating_unique',
            )
        ]

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'.strip()


class GroupMedia(BaseModelMedia):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа',
    )

    class Meta:
        default_related_name = 'media'
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'
