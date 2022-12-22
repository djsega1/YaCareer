from django.core.exceptions import ValidationError
from django.test import TestCase

from posts.models import GroupVacancy


class TestsForModels(TestCase):
    fixtures = ['fixtures/data.json', ]

    def test_invalid_vacancy(self):
        test_data = [
            {
                'text': 'SUPERDEScription1235$@#!@#',
                'group_id': 123,
            },
            {
                'text': 'nikita12352345!!',
                'group_id': None,
            },
        ]
        for data_set in test_data:
            vacancy_count = GroupVacancy.objects.count()
            with self.assertRaises(ValidationError):
                new_vacancy = GroupVacancy(
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
                'text': 'SUPERDEScription1235$@#!@#',
                'group_id': 1,
            },
            {
                'text': 'nikita12352345!!',
                'group_id': 1,
            },
        ]
        vacancy_count = GroupVacancy.objects.count()
        for data_set in test_data:
            new_vacancy = GroupVacancy(
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
