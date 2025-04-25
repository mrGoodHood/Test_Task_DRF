from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('ad_sender', 'created_at')
