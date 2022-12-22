from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_endpoints(self):
        endpoints = {
            200: [
                'description',
            ],
        }
        for url in endpoints[200]:
            response = self.client.get(reverse(f'about:{url}'))
            self.assertEqual(
                response.status_code,
                200,
            )
