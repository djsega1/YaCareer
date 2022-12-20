from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class TestsForModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email='client@gmail.com',
            password='fakfjknawef1323'
        )

    def test_invalid(self):
        user_count = User.objects.count()
        for text in (
            'client@gmail.com',
            'bad_mail.com',
            'check_validation_of_email',
        ):
            with self.assertRaises(ValidationError):
                new_user = User(
                    email=text,
                    password='asfhgsg32afds',
                )
                new_user.full_clean()
                new_user.save()
            self.assertEqual(
                User.objects.count(),
                user_count,
            )

    def test_valid(self):
        user_count = User.objects.count()
        for i, text in enumerate((
            'mail1@gmail.com',
            'mail2@yandex.ru',
            'mail3@mail.ru',
        ), start=1):
            new_user = User(
                email=text,
                password='asfhgsg32afds',
            )
            new_user.full_clean()
            new_user.save()
        self.assertEqual(
            User.objects.count(),
            user_count + i,
        )

    def tearDown(self):
        User.objects.all().delete()
        super().tearDown()
