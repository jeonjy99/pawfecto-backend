from django.db import models
from django.conf import settings


# -----------------------------------------------------------
# StyleTag (공통 스타일 태그 모델)
# -----------------------------------------------------------
class StyleTag(models.Model):
    code = models.CharField(max_length=50, unique=True)   # 영문 코드명
    name = models.CharField(max_length=50)                # 한국어 태그명 또는 표시용 이름

    def __str__(self):
        return self.name


# -----------------------------------------------------------
# 2. Campaign (캠페인)
# -----------------------------------------------------------

class Campaign(models.Model):
    """
    광고 캠페인 정보 모델입니다.
    SQL 스키마와 100% 동일하게 반영한 버전입니다.
    """
    campaign_id = models.AutoField(primary_key=True)

    brand = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='campaigns'
    )

    product_name = models.CharField(max_length=100)
    product_image_url = models.CharField(max_length=255)
    product_description = models.TextField()

    # ENUM('dog', 'cat') NULL
    target_pet_type = models.CharField(
        max_length=10,
        choices=[('dog', 'Dog'), ('cat', 'Cat')],
        null=True,
        blank=True
    )

    min_follower_count = models.IntegerField(default=0)

    requested_at = models.DateTimeField()
    application_deadline_at = models.DateField()

    # SQL은 DATE 타입 → Django에서는 DateField 그대로 유지
    posting_start_at = models.DateField()
    posting_end_at = models.DateField()

    required_creator_count = models.IntegerField()

    # 캠페인 스타일 태그 (StyleTag.code 값 1개 저장)
    style_tag = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.product_name



# -----------------------------------------------------------
# 3. CampaignAcceptance (캠페인 신청 / 수락)
# -----------------------------------------------------------

class CampaignAcceptance(models.Model):
    """
    크리에이터의 캠페인 신청 및 수락 상태를 관리하는 모델입니다.
    SQL 스키마 기준으로 정확히 반영했습니다.
    """
    campaign_acceptance_id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='campaign_acceptances'
    )

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='acceptances'
    )

    # ENUM('pending', 'accepted', 'rejected', 'completed')
    acceptance_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )

    applied_at = models.DateTimeField(null=True, blank=True)  # SQL: DATETIME (auto_now_add 아님)
    accepted_at = models.DateTimeField(null=True, blank=True)  # SQL 스키마와 동일하게 수정

    def __str__(self):
        return f"{self.creator.name} - {self.campaign.product_name} ({self.acceptance_status})"


# -----------------------------------------------------------
# 4. Deliverable (포스팅 결과물)
# -----------------------------------------------------------

class Deliverable(models.Model):
    """
    크리에이터가 제출한 포스팅 결과물(납품) 정보 모델입니다.
    SQL 스키마와 동일하게 구성.
    """
    deliverable_id = models.AutoField(primary_key=True)

    campaign_acceptance = models.ForeignKey(
        CampaignAcceptance,
        on_delete=models.CASCADE,
        related_name='deliverables'
    )

    posted_at = models.DateTimeField(null=True, blank=True)  # SQL은 auto_now_add 아님
    post_url = models.CharField(max_length=255, null=True, blank=True)

    # ENUM('incomplete', 'completed')
    deliverable_status = models.CharField(
        max_length=10,
        choices=[
            ('incomplete', 'Incomplete'),
            ('completed', 'Completed'),
        ],
        default='incomplete'
    )

    def __str__(self):
        return f"Deliverable for {self.campaign_acceptance.campaign.product_name}"

