from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdModelTest(TestCase):
    def test_create_ad(self):
        user = User.objects.create_user(username='testuser')
        ad = Ad.objects.create(user=user, title="Phone", description="Old phone", category="Electronics", condition="Used")
        self.assertEqual(str(ad), ad.title)
        self.assertIsNotNone(ad.created_at)

class ExchangeProposalTest(TestCase):
    def test_create_proposal(self):
        user = User.objects.create_user(username='testuser')
        ad1 = Ad.objects.create(user=user, title="Phone", description="Old", category="Tech", condition="Used")
        ad2 = Ad.objects.create(user=user, title="Book", description="Sci-Fi", category="Books", condition="New")
        proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, comment="Want to trade")
        self.assertEqual(proposal.status, "ожидает")
