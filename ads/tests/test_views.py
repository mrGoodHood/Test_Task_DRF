from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad

class AdViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.client.login(username='tester', password='testpass')
        self.ad = Ad.objects.create(user=self.user, title="Bike", description="Mountain", category="Transport", condition="Used")

    def test_edit_own_ad(self):
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Updated Bike',
            'description': 'Updated desc',
            'category': 'Transport',
            'condition': 'Used',
        })
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Bike')

    def test_delete_ad(self):
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())
