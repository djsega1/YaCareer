from django.db import models


class NamedModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')

    class Meta:
        abstract = True
        verbose_name = 'именованный объект'


class City(NamedModel):
    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self) -> str:
        return self.name


class University(NamedModel):
    description = models.CharField(max_length=300, verbose_name='описание')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'университет'
        verbose_name_plural = 'университеты'

    def __str__(self) -> str:
        return self.name


class Specialization(NamedModel):
    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'

    def __str__(self) -> str:
        return self.name


class Tag(NamedModel):
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self) -> str:
        return self.name


class Faculty(NamedModel):
    description = models.CharField(max_length=300, verbose_name='описание')
    specialization = models.ForeignKey(
        Specialization, on_delete=models.DO_NOTHING
    )
    tags = models.ManyToManyField(Tag)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'факультет'
        verbose_name_plural = 'факультеты'

    def __str__(self) -> str:
        return self.name


class TestResult(models.Model):
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'результаты теста'
        verbose_name_plural = 'результаты тестов'

    def __str__(self) -> str:
        return self.name


class Test(models.Model):
    question = models.CharField(max_length=300, verbose_name='вопрос')
    variant_a = models.CharField(max_length=300, verbose_name='вопрос')
    variant_b = models.CharField(max_length=300, verbose_name='вопрос')

    class Meta:
        verbose_name = 'тест'

    def __str__(self) -> str:
        return self.name
