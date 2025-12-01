from rest_framework import serializers
from .models import Campaign, CampaignAcceptance, Deliverable
from accounts.serializers import UserSerializer


# -----------------------------------------------------------
# 1. CampaignSerializer
# -----------------------------------------------------------

class CampaignSerializer(serializers.ModelSerializer):
    brand = UserSerializer(read_only=True)  # 브랜드 정보 포함

    class Meta:
        model = Campaign
        fields = [
            'campaign_id',
            'brand',
            'product_name',
            'product_image_url',
            'product_description',
            'target_pet_type',
            'min_follower_count',
            'style_tags',                # 수정: style_tag → style_tags
            'requested_at',
            'application_deadline_at',
            'posting_start_at',
            'posting_end_at',
            'required_creator_count',
        ]


# -----------------------------------------------------------
# 2. CampaignListSerializer (요약용)
# -----------------------------------------------------------

class CampaignListSerializer(serializers.ModelSerializer):
    brand = UserSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'campaign_id',
            'product_name',
            'brand',
            'product_image_url',
            'requested_at',
            'application_deadline_at',
        ]


# -----------------------------------------------------------
# 3. CampaignAcceptanceSerializer
# -----------------------------------------------------------

class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    campaign = CampaignListSerializer(read_only=True)

    class Meta:
        model = CampaignAcceptance
        fields = [
            'campaign_acceptance_id',
            'creator',
            'campaign',
            'acceptance_status',
            'applied_at',
            'accepted_at',      # 수정: accpeted_at → accepted_at
        ]


# -----------------------------------------------------------
# 4. DeliverableSerializer
# -----------------------------------------------------------

class DeliverableSerializer(serializers.ModelSerializer):
    campaign_acceptance = CampaignAcceptanceSerializer(read_only=True)

    class Meta:
        model = Deliverable
        fields = [
            'deliverable_id',
            'campaign_acceptance',
            'posted_at',
            'post_url',
            'deliverable_status',
        ]
