from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from .models import Campaign, CampaignAcceptance
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignAcceptanceSerializer,
)

from accounts.models import User
from accounts.serializers import CreatorSerializer


# ########################
# 캠페인 관련
# ########################

# -----------------------------------------------------------
# 1. 캠페인 생성 (POST /campaigns/create/)
# -----------------------------------------------------------

@api_view(['GET', 'POST'])
def create_campaign(request):
    # GET: 테스트용 응답
    if request.method == 'GET':
        return Response({"message": "캠페인 생성 엔드포인트"}, status=200)

    # POST: 캠페인 생성
    if request.method == 'POST':
        brand = request.user

        if brand.account_type != 'brand':
            return Response({"error": "브랜드 계정만 가능합니다."}, status=403)

        data = request.data.copy()
        data["brand"] = brand.id

        serializer = CampaignSerializer(data=data)
        if serializer.is_valid():
            serializer.save(brand=brand)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# -----------------------------------------------------------
# 2. 캠페인 상세 조회 (GET /campaigns/<id>/)
# -----------------------------------------------------------

@api_view(['GET'])
def campaign_detail(request, id):
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data)


# -----------------------------------------------------------
# 3. 캠페인 수정 (PUT /campaigns/<id>/update/)
# -----------------------------------------------------------

@api_view(['PUT'])
def update_campaign(request, id):
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CampaignSerializer(campaign, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "campaign updated", "campaign": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
# 4. 브랜드 캠페인 삭제 (DELETE /campaigns/<id>/delete/)
# -----------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_campaign(request, id):

    # 1) 캠페인 존재 여부 확인
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    # 2) 브랜드 타입인지 확인
    if request.user.account_type != "brand":
        return Response({"error": "Only brand accounts can delete campaigns."},
                        status=status.HTTP_403_FORBIDDEN)

    # 3) 자신의 캠페인인지 확인
    if campaign.brand_id != request.user.id:
        return Response({"error": "You do not have permission to delete this campaign."},
                        status=status.HTTP_403_FORBIDDEN)

    # 4) 삭제
    campaign.delete()

    return Response({"message": "campaign deleted successfully"}, status=status.HTTP_200_OK)

# -----------------------------------------------------------
# 5. 브랜드 캠페인 목록 (GET /brands/<brand_id>/campaigns/)
# -----------------------------------------------------------

@api_view(['GET'])
def brand_campaigns(request, brand_id):
    campaigns = Campaign.objects.filter(brand_id=brand_id).order_by('-requested_at')
    serializer = CampaignListSerializer(campaigns, many=True)
    return Response(serializer.data)


# -----------------------------------------------------------
# 6. 크리에이터가 받은 오퍼 목록 (GET /creators/<creator_id>/offers/)
# -----------------------------------------------------------

@api_view(['GET'])
def creator_offers(request, creator_id):
    """
    acceptance_status = 'pending' 또는 'accepted' 만 오퍼로 간주
    """
    acceptances = CampaignAcceptance.objects.filter(
        creator_id=creator_id,
        acceptance_status__in=['pending', 'accepted']
    )

    serializer = CampaignAcceptanceSerializer(acceptances, many=True)
    return Response(serializer.data)


# -----------------------------------------------------------
# 7. 크리에이터 진행중 캠페인 목록 (GET /creators/<creator_id>/progress/)
# -----------------------------------------------------------

@api_view(['GET'])
def creator_progress(request, creator_id):
    """
    진행중: acceptance_status = 'accepted'
    """
    acceptances = CampaignAcceptance.objects.filter(
        creator_id=creator_id,
        acceptance_status='accepted'
    )

    serializer = CampaignAcceptanceSerializer(acceptances, many=True)
    return Response(serializer.data)



# ########################
# 크리에이터 추천 기능
# ########################
# -----------------------------------------------------------
# 캠페인 기반 크리에이터 추천
# GET /campaigns/<id>/recommendations/
# -----------------------------------------------------------

@api_view(['GET'])
def recommend_creators(request, id):

    # 1) 캠페인 가져오기
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    # 2) 기본 필터 적용
    creators = User.objects.filter(
        account_type="creator",
        pet_type=campaign.target_pet_type,
        follower_count__gte=campaign.min_follower_count
    )

    # 3) 스타일 태그 필터링 (둘 다 no_preference면 스킵)
    if (
        campaign.style_tags 
        and campaign.style_tags != "no_preference"
    ):
        creators = creators.filter(style_tags=campaign.style_tags)

    # 4) 추천된 크리에이터 직렬화
    serializer = CreatorSerializer(creators, many=True)

    return Response({
        "campaign_id": campaign.campaign_id,
        "recommended_count": creators.count(),
        "recommended_creators": serializer.data
    }, status=status.HTTP_200_OK)



# ########################
# 캠페인 신청/수락 API 추가
# ########################
# -----------------------------------------------------------
# 1. 브랜드가 크리에이터에게 초대 (POST /campaigns/<id>/invite/)
# -----------------------------------------------------------
@api_view(['POST'])
def invite_creator(request, id):
    creator_id = request.data.get("creator_id")

    # 캠페인 확인
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    # 초대할 크리에이터 확인
    try:
        creator = User.objects.get(id=creator_id, account_type="creator")
    except User.DoesNotExist:
        return Response({"error": "Creator not found"}, status=status.HTTP_404_NOT_FOUND)

    # 기존 신청 내역 존재 여부 확인
    acceptance, created = CampaignAcceptance.objects.get_or_create(
        campaign=campaign,
        creator=creator,
        defaults={
            "acceptance_status": "pending",
            "applied_at": timezone.now(),
        }
    )

    # 이미 있었다면 상태만 업데이트
    if not created:
        acceptance.acceptance_status = "pending"
        acceptance.applied_at = timezone.now()
        acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response({
        "message": "creator invited",
        "created": created,
        "acceptance": serializer.data
    }, status=status.HTTP_200_OK)


# -----------------------------------------------------------
# 2. 크리에이터가 참가 수락 (POST /campaigns/<id>/accept/)
# -----------------------------------------------------------
@api_view(['POST'])
def accept_campaign(request, id):
    creator_id = request.data.get("creator_id")

    # 캠페인 확인
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    # 크리에이터 확인
    try:
        creator = User.objects.get(id=creator_id, account_type="creator")
    except User.DoesNotExist:
        return Response({"error": "Creator not found"}, status=status.HTTP_404_NOT_FOUND)

    # 신청 기록 확인
    try:
        acceptance = CampaignAcceptance.objects.get(campaign=campaign, creator=creator)
    except CampaignAcceptance.DoesNotExist:
        return Response({"error": "Invitation not found"}, status=status.HTTP_404_NOT_FOUND)

    # 상태 업데이트
    acceptance.acceptance_status = "accepted"
    acceptance.accepted_at = timezone.now()
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response({
        "message": "campaign accepted",
        "acceptance": serializer.data
    }, status=status.HTTP_200_OK)


# -----------------------------------------------------------
# 3. 크리에이터가 참가 거절 (POST /campaigns/<id>/reject/)
# -----------------------------------------------------------
@api_view(['POST'])
def reject_campaign(request, id):
    creator_id = request.data.get("creator_id")

    # 캠페인 확인
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    # 크리에이터 확인
    try:
        creator = User.objects.get(id=creator_id, account_type="creator")
    except User.DoesNotExist:
        return Response({"error": "Creator not found"}, status=status.HTTP_404_NOT_FOUND)

    # 신청 기록 확인
    try:
        acceptance = CampaignAcceptance.objects.get(campaign=campaign, creator=creator)
    except CampaignAcceptance.DoesNotExist:
        return Response({"error": "Invitation not found"}, status=status.HTTP_404_NOT_FOUND)

    # 거절
    acceptance.acceptance_status = "rejected"
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response({
        "message": "campaign rejected",
        "acceptance": serializer.data
    }, status=status.HTTP_200_OK)
