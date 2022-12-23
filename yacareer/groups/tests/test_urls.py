from django.test import TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    fixtures = ('fixtures/data.json',)

    def test_registration_endpoints(self):
        endpoints = {
            200: (
                'group_list',
                'create',
            ),
            '200 with args': (
                'edit',
                'delete',
                'group_detail',
            ),
        }

        for url in endpoints[200]:
            with self.subTest(f'Success url - {url}'):
                response = self.client.get(reverse(f'groups:{url}'))
                self.assertEqual(response.status_code, 200)

        for url in endpoints['200 with args']:
            with self.subTest(f'Success url - {url}'):
                response = self.client.get(reverse(f'groups:{url}', args=(1,)))
                self.assertEqual(response.status_code, 200)
