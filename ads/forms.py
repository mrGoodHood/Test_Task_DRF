from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    """Создания и редактирования объявления."""
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
