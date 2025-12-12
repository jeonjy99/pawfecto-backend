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

    # style_tags 읽기용(nested)
    style_tags = StyleTagSerializer(many=True, read_only=True)

    # 쓰기용(PK 배열)
    style_tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=StyleTag.objects.all(),
        write_only=True,
        required=False
    )

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
            'style_tags',        # 읽기 전용 태그 목록
            'style_tag_ids',     # 쓰기용 ID 목록
            'requested_at',
            'application_deadline_at',
            'posting_start_at',
            'posting_end_at',
            'required_creator_count',
        ]


    # create 오버라이드: style_tags M2M 저장 처리
    def create(self, validated_data):
        tag_ids = validated_data.pop("style_tag_ids", [])

        # 캠페인 생성
        campaign = Campaign.objects.create(**validated_data)

        # 태그 선택이 없으면 no_preference 자동 적용
        if not tag_ids:
            no_pref = StyleTag.objects.get(code="no_preference")
            tag_ids = [no_pref]

        campaign.style_tags.set(tag_ids)

        return campaign


    # update 오버라이드: 부분 업데이트 처리
    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("style_tag_ids", None)

        # 일반 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 태그 수정 요청이 있을 때만 처리
        if tag_ids is not None:
            if not tag_ids:
                no_pref = StyleTag.objects.get(code="no_preference")
                tag_ids = [no_pref]
            instance.style_tags.set(tag_ids)

        return instance



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
