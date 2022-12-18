from django.db import models


class BaseModel(models.Model):
    description = models.CharField(
        'описание',
        max_length=1024,
    )
    avatar = models.ImageField(
        'аватар',
        default='static_dev/img/user.png',
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    name = models.CharField(
        'название',
        max_length=70,
    )
    slug = models.SlugField(
        'ссылка',
        max_length=2048,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseMedia(models.Model):
    name = models.CharField(
        'название',
        max_length=256,
    )
    description = models.CharField(
        'описание',
        max_length=4096,
    )
    file = models.FileField(
        'media',
        upload_to='files',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
