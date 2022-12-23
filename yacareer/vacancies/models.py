from django.db import models

from groups.models import Group


class GroupVacancy(models.Model):
    vacancy_name = models.CharField(
        'название',
        max_length=70,
    )
    text = models.CharField(
        'текст к посту',
        max_length=1024,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа',
    )

    class Meta:
        ordering = ['id']
        default_related_name = 'group_vacancy'
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'

    def __str__(self):
        return self.vacancy_name
