from rest_framework import serializers

from .models import AccountBrand, AccountCreator, Campaign, CampaignAcceptance, Deliverable


class AccountBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBrand
        fields = '__all__'


class AccountCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCreator
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignAcceptance
        fields = '__all__'


class DeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverable
        fields = '__all__'

