from django.db import models
# from django.utils import timezone # <- auto_now_add를 사용하므로 timezone은 불필요합니다.

# -----------------------------------------------------------
# 1. Account (Brand + Creator 통합)
# -----------------------------------------------------------

class Account(models.Model):
    """
    브랜드와 크리에이터 계정을 통합 관리하는 모델입니다.
    """
    ACCOUNT_TYPES = [
        ('brand', 'Brand (광고주)'),
        ('creator', 'Creator (인플루언서)'),
    ]

    # 기본 계정 정보
    account_id = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)
    
    # 로그인 및 식별 정보 (UNIQUE 및 NOT NULL 제약 조건 반영)
    login_id = models.CharField(max_length=50, unique=True, null=False)
    login_password = models.CharField(max_length=50, null=False) # 실제 운영 시 해시 함수 사용 필수
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

    class Meta:
        verbose_name = "계정"
        verbose_name_plural = "계정 목록"

    def __str__(self):
        return f"[{self.account_type.upper()}] {self.name} ({self.login_id})"

# -----------------------------------------------------------
# 2. Campaign (캠페인)
# -----------------------------------------------------------

class Campaign(models.Model):
    """
    광고 캠페인 정보 모델입니다.
    """
    campaign_id = models.AutoField(primary_key=True)
    
    # FK 연결: Brand ID -> Account
    brand = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        limit_choices_to={'account_type': 'brand'},
        related_name='campaigns_as_brand'
    )
    
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=100, null=True, blank=True)
    product_image_url = models.CharField(max_length=255, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    target_pet_type = models.CharField(max_length=100, null=True, blank=True)
    min_follower_count = models.IntegerField(null=True, blank=True)
    
    # 시간 필드: 요청 등록일 (생성 시 한 번만 기록)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    # 시간 필드 (DATETIME 타입 반영)
    application_deadline_at = models.DateTimeField(null=True, blank=True)
    posting_start_at = models.DateTimeField(null=True, blank=True)
    posting_end_at = models.DateTimeField(null=True, blank=True)
    
    required_creator_count = models.IntegerField(null=True, blank=True)
    
    # 캠페인 상태 필드 추가 (운영 효율성 보강)
    campaign_status = models.CharField(max_length=20, default='DRAFT') 

    class Meta:
        verbose_name = "캠페인"
        verbose_name_plural = "캠페인 목록"
    
    def __str__(self):
        return self.product_name


# -----------------------------------------------------------
# 3. CampaignAcceptance (캠페인 참여/수락)
# -----------------------------------------------------------

class CampaignAcceptance(models.Model):
    """
    크리에이터의 캠페인 신청 및 수락 상태를 관리하는 모델입니다.
    """
    campaign_acceptance_id = models.AutoField(primary_key=True)
    
    # FK 연결: Creator ID -> Account
    creator = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        limit_choices_to={'account_type': 'creator'},
        related_name='applications_as_creator'
    )
    # FK 연결: Campaign ID -> Campaign
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    acceptance_status = models.CharField(max_length=100, null=True, blank=True)
    
    # 신청 일시: 모델 생성 시점 한 번만 자동 기록
    applied_at = models.DateTimeField(auto_now_add=True)
    
    # 선정 시점: 수동으로 기록
    selected_at = models.DateTimeField(null=True, blank=True) 

    class Meta:
        # 중복 신청 방지 제약 조건
        unique_together = ('creator', 'campaign')
        verbose_name = "캠페인 참여 정보"
        verbose_name_plural = "캠페인 참여 정보 목록"

    def __str__(self):
        return f"{self.creator.name} - {self.campaign.product_name} ({self.acceptance_status})"


# -----------------------------------------------------------
# 4. Deliverable (포스팅 결과물)
# -----------------------------------------------------------

class Deliverable(models.Model):
    """
    크리에이터가 제출한 포스팅 결과물(납품) 정보 모델입니다.
    """
    deliverable_id = models.AutoField(primary_key=True)
    
    # FK 연결: Campaign Acceptance ID -> CampaignAcceptance
    acceptance = models.ForeignKey(
        CampaignAcceptance, 
        on_delete=models.CASCADE, 
        related_name='deliverables'
    )
    
    # 포스팅 일시: 결과물 레코드 생성 시점 한 번만 자동 기록
    posted_at = models.DateTimeField(auto_now_add=True) 
    
    post_url = models.CharField(max_length=255, null=True, blank=True)
    deliverable_status = models.CharField(max_length=100, null=True, blank=True)
    
    # 정산 관련 필드 추가 (운영 효율성 보강)
    brand_approval_at = models.DateTimeField(null=True, blank=True)
    settlement_status = models.CharField(max_length=20, default='PENDING')

    class Meta:
        verbose_name = "결과물"
        verbose_name_plural = "결과물 목록"
    
    def __str__(self):
        return f"Deliverable for {self.acceptance.campaign.product_name}"