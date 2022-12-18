from django.db import models

from core.models import BaseModelImage


class Service(BaseModelImage):
    name = models.CharField(max_length=150, verbose_name='сервис')

    class Meta:
        verbose_name = 'сервис'
        verbose_name_plural = 'сервисы'
        default_related_name = 'service'
