from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('brand', 'Brand (광고주)'),
        ('creator', 'Creator (인플루언서)'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Brand 전용 필드
    brand_pet_focus = models.CharField(max_length=100, null=True, blank=True)

    # Creator 전용 필드
    address = models.TextField(null=True, blank=True)
    pet_type = models.CharField(max_length=100, null=True, blank=True)
    sns_handle = models.CharField(max_length=50, null=True, blank=True)
    sns_url = models.CharField(max_length=255, null=True, blank=True)
    total_post_count = models.IntegerField(null=True, blank=True)
    follower_count = models.IntegerField(null=True, blank=True)
    
    # 이미지 URL 필드 추가
    profile_image_url = models.CharField(max_length=255, null=True, blank=True)

    # <Object: 8sdfx>
    # __str__ : 객체를 print할 때 커스터마이징
    def __str__(self):
        return f"[{self.account_type.upper()}] {self.name} ({self.username})"
    
