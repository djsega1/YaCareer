from django import forms

from core.forms import BaseModelForm
from vacancies.models import GroupVacancy


class GroupVacancyForm(BaseModelForm):

    class Meta:
        model = GroupVacancy
        fields = ('v_name', 'text',)


class RespondForm(forms.Form):
    text = forms.CharField(
        label='Текст письма (расскажите о себе)',
        max_length=1024,
    )
