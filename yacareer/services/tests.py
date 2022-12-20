from django.core.exceptions import ValidationError
from django.test import TestCase

from services.models import Service


class TestsForModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = Service.objects.create(
            name='test',
            bootstrap_icon='some icon',
        )

    def test_invalid(self):
        service_count = Service.objects.count()
        test_data = (
            {
                "name": "test",
                "bootstrap_icon": "bi bi-0-square",
            },
            {
                "name": "test2",
                "bootstrap_icon": None,
            },
            {
                "name": None,
                "bootstrap_icon": "bi bi-0-square",
            },
        )
        for data_set in test_data:
            with self.assertRaises(ValidationError):
                new_service = Service(
                    name=data_set['name'],
                    bootstrap_icon=data_set['bootstrap_icon']
                )
                new_service.full_clean()
                new_service.save()
            self.assertEqual(
                Service.objects.count(),
                service_count,
            )

    def test_valid(self):
        service_count = Service.objects.count()
        test_data = (
            {
                "name": "test2",
                "bootstrap_icon": "bi bi-0-square",
            },
            {
                "name": "SUPER@TEST",
                "bootstrap_icon": "some icon",
            },
            {
                "name": "123456",
                "bootstrap_icon": "partick bateman",
            },
        )
        for data_set in test_data:
            new_service = Service(
                name=data_set['name'],
                bootstrap_icon=data_set['bootstrap_icon']
            )
            new_service.full_clean()
            new_service.save()
        self.assertEqual(
            Service.objects.count(),
            service_count + len(test_data),
        )

    def tearDown(self):
        Service.objects.all().delete()
        super().tearDown()
