from django.db import models


class Service(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='сервис',
        unique=True,
    )
    bootstrap_icon = models.CharField(
        max_length=150,
        verbose_name='иконка',
        help_text='https://icons.bootstrap-5.ru/icons/'
                  'Найдите на данном сайте нужную картинку и впишите название'
                  '(например: bi bi-telegram)',
    )
    is_contact = models.BooleanField(
        'контакт',
        default=False,
    )

    class Meta:
        verbose_name = 'сервис'
        verbose_name_plural = 'сервисы'
        default_related_name = 'service'

    def __str__(self):
        return self.name
