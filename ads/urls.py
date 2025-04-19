from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('ads/search/', views.search_ads, name='search_ads'),
    path('proposals/create/', views.create_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/update/', views.update_proposal, name='update_proposal'),
    path('proposals/', views.view_proposals, name='view_proposals'),
]
