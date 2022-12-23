from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


class BaseModelImage(models.Model):
    photo = models.ImageField(
        'фото',
        upload_to='images/',
        blank=True,
    )

    class Meta:
        abstract = True

    @property
    def get_img(self):
        return get_thumbnail(
            self.photo,
            '200x200',
            crop='center',
            quality=51,
        )

    def image_tmb(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.get_img.url}">',
            )
        return 'Нет изображения'

    @property
    def get_img_small(self):
        return get_thumbnail(
            self.photo,
            '50x50',
            crop='center',
            quality=51
        )

    def image_tmb_small(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.get_img_small.url}">',
            )
        return 'Нет изображения'

    @property
    def get_img_logo(self):
        return get_thumbnail(
            self.photo,
            '30x30',
            crop='center',
            quality=51
        )

    def image_tmb_logo(self):
        if self.photo:
            return mark_safe(
                '<img class="rounded-circle border border-1 border-dark" '
                f'src="{self.get_img_logo.url}">',
            )
        return 'Нет изображения'

    image_tmb.short_description = 'превью'
    image_tmb.allow_tags = True
