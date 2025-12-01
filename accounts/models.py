from django.db import models
from django.contrib.auth.models import AbstractUser


# [강사님이 봐주신 코드]

# from django.contrib.auth.models import AbstractUser


'''
accounts_User
SELECT * FROM accounts_user
WHERE account_type = 'brand'

accounts_User
SELECT * FROM accounts_user
WHERE account_type = 'creator'

creators = User.objects.filter(acount_type="creator")
brands = User.objects.filter(acount_type="brand")
'''

# # Create your models here.
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('brand', 'Brand (광고주)'),
        ('creator', 'Creator (인플루언서)'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    pet_type = models.CharField(
        max_length=10,
        choices=[('dog', 'Dog'), ('cat', 'Cat')],
        null=True,
        blank=True
    )

    # Brand 전용 필드
    profile_image = models.ImageField(null=True, blank=True)

    # Creator 전용 필드
    address = models.TextField(null=True, blank=True)
    pet_type = models.CharField(max_length=100, null=True, blank=True)
    sns_handle = models.CharField(max_length=50, null=True, blank=True)
    sns_url = models.CharField(max_length=255, null=True, blank=True)
    total_post_count = models.IntegerField(null=True, blank=True)
    follower_count = models.IntegerField(null=True, blank=True)
    
    # ENUM('outdoor', 'energetic', ...)
    STYLE_TAG_CHOICES = [
        ('outdoor', 'Outdoor'),
        ('energetic', 'Energetic'),
        ('no_preference', 'No Preference'),
        ('minimal', 'Minimal'),
        ('aesthetic', 'Aesthetic'),
        ('heartfelt', 'Heartfelt'),
        ('cozy', 'Cozy'),
        ('wholesome', 'Wholesome'),
        ('funny', 'Funny'),
        ('calm', 'Calm'),
    ]

    style_tags = models.CharField(
        max_length=20,
        choices=STYLE_TAG_CHOICES,
        null=True,         # SQL 스키마 NULL 허용
        blank=True
    )

    # 이미지 URL 필드 추가
    profile_image_url = models.CharField(max_length=255, null=True, blank=True)


    # <Object: 8sdfx>
    # __str__ : 객체를 print할 때 커스터마이징
    def __str__(self):
        return f"[{self.account_type.upper()}] {self.name} ({self.username})"
    
