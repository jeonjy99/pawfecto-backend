from rest_framework import serializers
from .models import User
from myapp.models import StyleTag     # ← StyleTag는 myapp에 위치
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------------------------------------------
# StyleTag Serializer (읽기용)
# -----------------------------------------------------------
class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'code', 'name']



# -----------------------------------------------------------
# BRAND 회원가입 Serializer
# -----------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'name',
            'phone_number',
            'pet_type',
            'profile_image_url',
            'account_type',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get("account_type") != "brand":
            raise serializers.ValidationError("This serializer is for brand accounts only.")

        required_fields = ['username', 'password', 'email', 'name', 'phone_number']

        for field in required_fields:
            if field not in data or data[field] in ["", None]:
                raise serializers.ValidationError(f"{field} is required for brand signup.")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



# -----------------------------------------------------------
# CREATOR 회원가입 Serializer
# -----------------------------------------------------------
class CreatorSerializer(serializers.ModelSerializer):

    # style_tags는 ID 배열로 받도록 설정
    style_tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=StyleTag.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'name',
            'sns_handle',
            'sns_url',
            'address',
            'style_tags',
            'account_type',
            'pet_type',
            'profile_image_url',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get("account_type") != "creator":
            raise serializers.ValidationError("This serializer is for creator accounts only.")

        required_fields = ['username', 'password', 'email', 'name', 'sns_handle', 'sns_url', 'address']

        for field in required_fields:
            if field not in data or data[field] in ["", None]:
                raise serializers.ValidationError(f"{field} is required for creator signup.")

        return data


    def create(self, validated_data):
        # style_tags를 먼저 분리
        style_tags = validated_data.pop("style_tags", [])

        # creator 생성
        user = User.objects.create_user(**validated_data)

        # 선택된 태그가 없으면 no_preference 적용
        if not style_tags:
            no_pref = StyleTag.objects.get(code="no_preference")
            style_tags = [no_pref]

        # M2M 저장
        user.style_tags.set(style_tags)

        return user



# -----------------------------------------------------------
# 기본 UserSerializer (읽기 전용 뷰 등에서 사용)
# -----------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    style_tags = StyleTagSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
