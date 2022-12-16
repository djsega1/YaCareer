from django.db import models
from core.models import Specialization


class Survey(models.Model):
    question = models.CharField(max_length=300, verbose_name='вопрос')
    variant_a = models.CharField(max_length=300, verbose_name='ответ 1')
    variant_b = models.CharField(max_length=300, verbose_name='ответ 2')

    class Meta:
        verbose_name = 'Тест'

    def __str__(self) -> str:
        return self.question


class TestResult(models.Model):
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'результаты теста'
        verbose_name_plural = 'результаты тестов'

    def __str__(self) -> str:
        return "Результаты теста"
