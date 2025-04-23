from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ads.models import Ad

class AdAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client.login(username='apiuser', password='apipass')

    def test_create_ad_via_api(self):
        response = self.client.post('/api/ads/', {
            'title': 'Laptop',
            'description': 'Old Mac',
            'category': 'Tech',
            'condition': 'Used',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
