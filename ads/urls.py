from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import html_views
from .api_views import AdViewSet, ExchangeProposalViewSet

# Роутер DRF
router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'exchange-proposals', ExchangeProposalViewSet, basename='exchangeproposal')

urlpatterns = [
    path('', html_views.home, name='home'),
    path('ads/create/', html_views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', html_views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', html_views.delete_ad, name='delete_ad'),
    path('ads/search/', html_views.search_ads, name='search_ads'),
    path('ads/<int:ad_id>/', html_views.ad_detail, name='ad_detail'),
    path('proposals/create/', html_views.create_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/update/', html_views.update_proposal, name='update_proposal'),
    path('proposals/', html_views.view_proposals, name='view_proposals'),
    path('api/', include(router.urls)),
]
