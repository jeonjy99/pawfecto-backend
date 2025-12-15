from django.db import models
from django.contrib.auth.models import AbstractUser
from myapp.models import StyleTag


# -----------------------------------
# User 모델 (Brand / Creator 통합)
# -----------------------------------
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('brand', 'Brand (광고주)'),
        ('creator', 'Creator (인플루언서)'),
    ]

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    pet_type = models.CharField(
        max_length=10,
        choices=[('dog', 'Dog'), ('cat', 'Cat')],
        null=True,
        blank=True
    )

    # Brand
    profile_image = models.ImageField(null=True, blank=True)
    profile_image_url = models.CharField(max_length=255, null=True, blank=True)

    # Creator
    address = models.TextField(null=True, blank=True)
    sns_handle = models.CharField(max_length=50, null=True, blank=True)
    sns_url = models.CharField(max_length=255, null=True, blank=True)
    total_post_count = models.IntegerField(null=True, blank=True)
    follower_count = models.IntegerField(null=True, blank=True)

    # 핵심: through 반드시 지정
    style_tags = models.ManyToManyField(
        StyleTag,
        through="UserStyleTag",
        related_name="users",
        blank=True
    )

    def __str__(self):
        return f"[{self.account_type.upper()}] {self.name} ({self.username})"


# -----------------------------------
# User ↔ StyleTag 중간 테이블
# -----------------------------------
class UserStyleTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    style_tag = models.ForeignKey(StyleTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "style_tag")

    def __str__(self):
        return f"{self.user_id} - {self.style_tag_id}"
