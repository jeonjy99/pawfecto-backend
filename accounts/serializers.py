from rest_framework import serializers
from .models import Brand, Creator


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'brand_id',
            'login_id',
            'name',
            'email',
            'phone_number',
            'pet_type',
            'profile_image_url',
        ]


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = [
            'creator_id',
            'login_id',
            'name',
            'email',
            'phone_number',
            'address',
            'pet_type',
            'sns_handle',
            'sns_url',
            'total_post_count',
            'follower_count',
            'style_tags',
            'profile_image_url',
        ]


# -----------------------------------------------------------
# 통합 UserSerializer (Brand/Creator 자동 구분)
# CampaignSerializer에서 brand=UserSerializer() 사용 가능
# CampaignAcceptanceSerializer에서도 creator=UserSerializer() 사용 가능
# -----------------------------------------------------------

class UserSerializer(serializers.Serializer):
    """
    Brand 또는 Creator 인스턴스를 자동으로 직렬화하는 통합 직렬화기
    """

    def to_representation(self, instance):
        # Brand인지 Creator인지 자동 판단
        if isinstance(instance, Brand):
            return BrandSerializer(instance).data
        elif isinstance(instance, Creator):
            return CreatorSerializer(instance).data
        else:
            return {}

