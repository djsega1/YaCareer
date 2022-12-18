from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import Profile


class TestsForModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.profile = Profile.objects.create(
            email='client@gmail.com',
            password='fakfjknawef1323',
        )

    def test_invalid(self):
        profile_count = Profile.objects.count()
        for text in (
            'client@gmail.com',
            'bad_mail.com',
            'check_validation_of_email',
        ):
            with self.assertRaises(ValidationError):
                new_profile = Profile(
                    email=text,
                    password='asfhgsg32afds',
                )
                new_profile.full_clean()
                new_profile.save()
            self.assertEqual(
                Profile.objects.count(),
                profile_count,
            )

    def test_valid(self):
        profile_count = Profile.objects.count()
        for i, text in enumerate((
            'mail1@gmail.com',
            'mail2@yandex.ru',
            'mail3@mail.ru',
        ), start=1):
            new_profile = Profile(
                email=text,
                password='asfhgsg32afds',
            )
            new_profile.full_clean()
            new_profile.save()
        self.assertEqual(
            Profile.objects.count(),
            profile_count + i,
        )

    def tearDown(self):
        Profile.objects.all().delete()
        super().tearDown()
