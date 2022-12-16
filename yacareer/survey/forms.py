from django import forms

from core.models import Specialization
from users.models import Profile
from .models import TestResult


class SurveyForm(forms.Form):
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

        for question in survey.questions:
            choices = [(choice.id, choice.text) for choice in question.choices]
            self.fields[f'question_{question.id}'] = \
                forms.ChoiceField(widget=forms.RadioSelect,
                                  choices=choices)
            self.fields[f'question_{question.id}'].label = question.text

    def survery_table(self, i, j):
        table = [
            [1, 2],
            [3, 4],
            [5, 1],
            [2, 3],
            [4, 5],
            [1, 3],
            [5, 2],
            [3, 5],
            [2, 4],
            [1, 4],
            [1, 2],
            [3, 4],
            [5, 1],
            [2, 3],
            [4, 5],
            [1, 3],
            [2, 5],
            [3, 5],
            [2, 4],
            [1, 4],
        ]
        return table[i][j]

    def calc(self, user, survey, data):
        res_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i, question in enumerate(survey.questions):
            result = data[f'question_{question.id}']
            ind = self.survery_table(i, int(result) - 1)
            res_dict[ind] += 1
        res = sorted(res_dict.items(), key=lambda item: item[1],
                     reverse=True)
        s = res[0][0]
        profile = Profile.objects.get(pk=user.id)
        if profile.test_result is None:
            specialization = Specialization.objects.get(pk=s)
            testResult = TestResult.objects \
                                   .create(specialization=specialization)
            testResult.save()
            profile.test_result = testResult
            profile.save()
        else:
            testResult = profile.test_result
            specialization = Specialization.objects.get(pk=s)
            testResult.specialization = specialization
            testResult.save()

    def save(self, user, survey):
        data = self.cleaned_data
        self.calc(user, survey, data)
