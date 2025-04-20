from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal
from django.urls import reverse


class AdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_create_ad(self):
        response = self.client.post(reverse('create_ad'), {
            'title': 'Ноутбук',
            'description': 'Состояние отличное',
            'category': 'Электроника',
            'condition': 'new',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(Ad.objects.first().title, 'Ноутбук')

    def test_edit_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Старый велосипед',
            description='Требует ремонта',
            category='Транспорт',
            condition='used',
        )
        response = self.client.post(reverse('edit_ad', args=[ad.id]), {
            'title': 'Велосипед',
            'description': 'На ходу',
            'category': 'Транспорт',
            'condition': 'used',
        })
        self.assertEqual(response.status_code, 302)
        ad.refresh_from_db()
        self.assertEqual(ad.title, 'Велосипед')


class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.ad1 = Ad.objects.create(user=self.user1, title='Книга', description='Новая', category='Книги', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Флешка', description='16GB', category='Электроника', condition='used')
        self.client = Client()
        self.client.login(username='user1', password='pass1')

    def test_create_proposal(self):
        response = self.client.post(reverse('create_proposal'), {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Давайте обменяемся',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(ExchangeProposal.objects.first().status, 'pending')

    def test_filter_proposals_by_status(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тест фильтра',
            status='accepted'
        )
        response = self.client.get(reverse('view_proposals') + '?status=accepted&mine=true')
        self.assertContains(response, 'Тест фильтра')
