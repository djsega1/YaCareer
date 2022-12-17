from django.test import TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_registration_endpoints(self):
        endpoints = {
            200: (
                'login',
                'logout',
                'password_reset',
                'password_reset_complete',
                'password_reset_done',
            ),
            302: (
                'password_change_done',
                'password_change',
            ),
        }

        for url in endpoints[200]:
            with self.subTest(f'Success url - {url}'):
                response = self.client.get(reverse(f'auth:{url}'))
                self.assertEqual(response.status_code, 200)

        for url in endpoints[302]:
            with self.subTest(f'Redirect url - {url}'):
                response = self.client.get(reverse(f'auth:{url}'))
                self.assertEqual(response.status_code, 302)
