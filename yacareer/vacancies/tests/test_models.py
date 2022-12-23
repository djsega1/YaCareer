from django.core.exceptions import ValidationError
from django.test import TestCase

from vacancies.models import GroupVacancy


class TestsForModels(TestCase):
    fixtures = ['fixtures/data.json', ]

    def test_invalid_vacancy(self):
        test_data = [
            {
                'vacancy_name':  'name_of_post',
                'text': 'SUPERDEScription1235$@#!@#',
                'group_id': 123,
            },
            {
                'vacancy_name':  'name_of_post2',
                'text': 'nikita12352345!!',
                'group_id': None,
            },
        ]
        for data_set in test_data:
            vacancy_count = GroupVacancy.objects.count()
            with self.assertRaises(ValidationError):
                new_vacancy = GroupVacancy(
                    vacancy_name=data_set['vacancy_name'],
                    text=data_set['text'],
                    group_id=data_set['group_id'],
                )
                new_vacancy.full_clean()
                new_vacancy.save()
            self.assertEqual(
                GroupVacancy.objects.count(),
                vacancy_count,
            )

    def test_valid_vacancy(self):
        test_data = [
            {
                'vacancy_name':  'name_of_post1',
                'text': 'SUPERDEScription1235$@#!@#',
                'group_id': 1,
            },
            {
                'vacancy_name':  'NikitaSuper',
                'text': 'nikita12352345!!',
                'group_id': 1,
            },
        ]
        vacancy_count = GroupVacancy.objects.count()
        for data_set in test_data:
            new_vacancy = GroupVacancy(
                vacancy_name=data_set['vacancy_name'],
                text=data_set['text'],
                group_id=data_set['group_id'],
            )
            new_vacancy.full_clean()
            new_vacancy.save()
        self.assertEqual(
            GroupVacancy.objects.count(),
            vacancy_count + len(test_data),
        )

    def tearDown(self):
        GroupVacancy.objects.all().delete()
        super().tearDown()
