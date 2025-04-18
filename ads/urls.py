from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
]