from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_registration_endpoints(self):
        # 'password_reset_confirm',
        endpoints = {
            200: [
                'login',
                'logout',
                'password_reset',
                'password_reset_complete',
                'password_reset_done',
            ],
            302: [
                'password_change_done',
                'password_change',
            ],
        }

        for url in endpoints[200]:
            with self.subTest(f'Succes url - {url}'):
                response = Client().get(reverse(f'auth:{url}'))
                self.assertEqual(response.status_code, 200)
