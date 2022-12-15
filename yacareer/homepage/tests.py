from django.test import TestCase


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(
            response.status_code,
            200,
        )
