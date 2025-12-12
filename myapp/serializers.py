from rest_framework import serializers
from .models import Campaign, CampaignAcceptance, Deliverable, StyleTag
from accounts.serializers import BrandSerializer, CreatorSerializer


# -----------------------------------------------------------
# StyleTag Serializer (공유)
# -----------------------------------------------------------
class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'code', 'name']



# -----------------------------------------------------------
# 1. CampaignSerializer (상세 페이지용)
# -----------------------------------------------------------

class CampaignSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

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
            'style_tag',              # 단일 스타일 태그
            'requested_at',
            'application_deadline_at',
            'posting_start_at',
            'posting_end_at',
            'required_creator_count',
        ]

    def validate_style_tag(self, value):
        if value is None:
            return value

        # StyleTag.code 유효성만 검증
        if not StyleTag.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid style_tag value.")

        return value



# -----------------------------------------------------------
# 2. CampaignListSerializer (요약 리스트용)
# -----------------------------------------------------------

class CampaignListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

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
# 3. CampaignAcceptanceSerializer (신청/수락 정보)
# -----------------------------------------------------------

class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)         # 신청한 크리에이터 정보
    campaign = CampaignListSerializer(read_only=True)   # 신청한 캠페인의 요약 정보

    class Meta:
        model = CampaignAcceptance
        fields = [
            'campaign_acceptance_id',
            'creator',
            'campaign',
            'acceptance_status',
            'applied_at',
            'accepted_at',
        ]



# -----------------------------------------------------------
# 4. DeliverableSerializer (납품 결과물)
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
