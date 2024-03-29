from django import forms

from core.forms import BaseModelForm
from vacancies.models import GroupVacancy


class GroupVacancyForm(BaseModelForm):

    class Meta:
        model = GroupVacancy
        fields = ('vacancy_name', 'text',)
        labels = {
            'vacancy_name': 'Название вакансии',
            'text': 'Описание обязанностей и требований',
        }


class RespondForm(forms.Form):
    text = forms.CharField(
        label='Текст письма (расскажите о себе)',
        max_length=1024,
    )
