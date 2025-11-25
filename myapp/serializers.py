from rest_framework import serializers
from .models import Campaign, CampaignAcceptance, Deliverable
from accounts.serializers import UserSerializer

# Campaign 직렬화기
class CampaignSerializer(serializers.ModelSerializer):
    brand = UserSerializer(read_only=True)  # 브랜드 정보 직렬화
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'brand', 'product_name', 'product_type', 'product_image_url', 'product_description',
                  'target_pet_type', 'min_follower_count', 'style_required', 'requested_at', 'application_deadline_at',
                  'posting_start_at', 'posting_end_at', 'required_creator_count']

# Campaign 리스트 직렬화기 (브랜드 정보 포함)
class CampaignListSerializer(serializers.ModelSerializer):
    brand = UserSerializer(read_only=True)  # 브랜드 정보 직렬화
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'product_name', 'product_type', 'brand', 'product_image_url', 'requested_at',
                  'application_deadline_at']

# CampaignAcceptance 직렬화기
class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)  # Creator 정보 직렬화
    campaign = CampaignListSerializer(read_only=True)  # Campaign 정보 직렬화
    class Meta:
        model = CampaignAcceptance
        fields = ['campaign_acceptance_id', 'creator', 'campaign', 'acceptance_status', 'applied_at', 'selected_at']

# Deliverable 직렬화기
class DeliverableSerializer(serializers.ModelSerializer):
    campaign_acceptance = CampaignAcceptanceSerializer(read_only=True)  # CampaignAcceptance 정보 직렬화
    class Meta:
        model = Deliverable
        fields = ['deliverable_id', 'campaign_acceptance', 'posted_at', 'post_url', 'deliverable_status']
