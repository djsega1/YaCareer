from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_endpoints(self):
        endpoints = {
            302: [
                'home',
            ],
        }
        for url in endpoints[302]:
            response = self.client.get(reverse(f'homepage:{url}'))
            self.assertEqual(
                response.status_code,
                302,
            )
