from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_endpoint(self):
        url = reverse('about:description')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
