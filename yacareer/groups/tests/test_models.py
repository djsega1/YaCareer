from django.core.exceptions import ValidationError
from django.test import TestCase

from groups.models import Group


class TestsForModels(TestCase):
    fixtures = ('fixtures/data.json',)

    def test_invalid(self):
        test_data = (
            {
                'name': 'Компания 3',
                'owner_id': 1,
            },
            {
                'name': '123',
                'owner_id': 0,
            },
        )
        group_count = Group.objects.count()
        for data_set in test_data:
            with self.assertRaises(ValidationError):
                new_group = Group(
                    name=data_set['name'],
                    owner_id=data_set['owner_id'],
                )
                new_group.full_clean()
                new_group.save()
            self.assertEqual(
                Group.objects.count(),
                group_count,
            )

    def test_valid(self):
        test_data = (
            {
                'name': 'super',
                'owner_id': 1,
            },
            {
                'name': 'TEST!@$@#$GROUP',
                'owner_id': 1,
            },
        )
        group_count = Group.objects.count()
        for data_set in test_data:
            new_group = Group(
                name=data_set['name'],
                owner_id=data_set['owner_id'],
            )
            new_group.full_clean()
            new_group.save()
        self.assertEqual(
            Group.objects.count(),
            group_count + len(test_data),
        )

    def tearDown(self):
        Group.objects.all().delete()
        super().tearDown()
