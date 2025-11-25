from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 기본 User 모델 가져오기
User = get_user_model()

# User 모델을 위한 직렬화기
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'account_type', 
                  'brand_pet_focus', 'address', 'pet_type', 'sns_handle', 'sns_url', 'total_post_count', 
                  'follower_count', 'style_profile']
