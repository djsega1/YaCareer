from django.db import models

from core.models import BaseModelPost
from groups.models import Group
from users.models import User


class UserPost(BaseModelPost):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )

    class Meta:
        default_related_name = 'user_post'
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class GroupVacancy(BaseModelPost):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа',
    )

    class Meta:
        default_related_name = 'group_post'
        verbose_name = 'пост'
        verbose_name_plural = 'посты'