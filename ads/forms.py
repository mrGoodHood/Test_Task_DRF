from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    """Форма для создания и редактирования объявления."""
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

class ProposalForm(forms.ModelForm):
    """Форма для создания предложения обмена."""
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
