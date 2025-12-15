from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Campaign, CampaignAcceptance, Deliverable
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignAcceptanceSerializer,
    DeliverableSerializer,
)
from accounts.models import User


# ============================================================
# 브랜드 기능
# ============================================================

# ------------------------------------------------------------
# 1) 브랜드 캠페인 목록 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brand_campaign_list(request, brand_id):

    if request.user.account_type != "brand":
        return Response({"error": "브랜드만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(brand_id):
        return Response({"error": "본인 캠페인만 조회 가능합니다."}, status=403)

    campaigns = Campaign.objects.filter(brand=request.user)
    serializer = CampaignListSerializer(campaigns, many=True)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 2) 캠페인 생성
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_campaign(request, brand_id):

    if request.user.account_type != "brand":
        return Response({"error": "브랜드만 캠페인을 생성할 수 있습니다."}, status=403)

    if request.user.id != brand_id:
        return Response({"error": "본인 브랜드로만 캠페인을 생성할 수 있습니다."}, status=403)

    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(brand=request.user)
        return Response(serializer.data, status=201)



# ------------------------------------------------------------
# 3) 캠페인 상세 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_detail(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 조회할 수 있습니다."}, status=403)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 4-1) 캠페인 수정
# ------------------------------------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_campaign(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인이 생성한 캠페인만 수정할 수 있습니다."}, status=403)

    serializer = CampaignSerializer(campaign, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 4-2) 캠페인 삭제
# ------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_campaign(request, brand_id, campaign_id):

    # 1. 캠페인 존재 여부 확인
    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    # 2. 브랜드 본인 여부 확인
    if campaign.brand != request.user:
        return Response(
            {"error": "본인이 생성한 캠페인만 삭제할 수 있습니다."},
            status=403
        )

    # 3. 삭제 실행
    campaign.delete()
    return Response({"message": "캠페인이 삭제되었습니다."}, status=204)


# ------------------------------------------------------------
# 5) 브랜드 입장에서 특정 캠페인에 대한 크리에이터 신청 현황 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_acceptance_list(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 조회할 수 있습니다."}, status=403)

    acceptances = CampaignAcceptance.objects.filter(campaign=campaign)
    serializer = CampaignAcceptanceSerializer(acceptances, many=True)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 6) 캠페인 진행 상황(Deliverable) 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_progress(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 진행 현황을 조회할 수 있습니다."}, status=403)

    deliverables = Deliverable.objects.filter(
        campaign_acceptance__campaign=campaign
    )

    serializer = DeliverableSerializer(deliverables, many=True)
    return Response(serializer.data, status=200)



# ============================================================
# 크리에이터 기능
# ============================================================

# ------------------------------------------------------------
# 7) 크리에이터 오퍼 조회 (CampaignAcceptance)
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def creator_campaign_offers(request, creator_id):

    if request.user.account_type != "creator":
        return Response({"error": "크리에이터만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(creator_id):
        return Response({"error": "본인 오퍼만 조회할 수 있습니다."}, status=403)

    offers = CampaignAcceptance.objects.filter(creator=request.user)
    serializer = CampaignAcceptanceSerializer(offers, many=True)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 8) 수락
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_campaign(request, creator_id, campaign_id):
    if request.user.id != creator_id:
        return Response(
            {"error": "본인의 캠페인만 수락할 수 있습니다."},
            status=403
        )

    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_id=campaign_id,   
        creator_id=creator_id,
        # acceptance_status="pending"
    )

    acceptance.acceptance_status = "accepted"
    acceptance.accepted_at = timezone.now()
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 9) 거절
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_campaign(request, creator_id, campaign_id):
    if request.user.id != creator_id:
        return Response(
            {"error": "본인의 캠페인만 거절할 수 있습니다."},
            status=403
        )

    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_id=campaign_id,
        creator_id=creator_id,
        # acceptance_status="pending"
    )

    acceptance.acceptance_status = "rejected"
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 10) 크리에이터 진행 상황 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def creator_progress(request, creator_id):

    if request.user.account_type != "creator":
        return Response({"error": "크리에이터만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(creator_id):
        return Response({"error": "본인 진행상황만 조회 가능합니다."}, status=403)

    deliverables = Deliverable.objects.filter(
        campaign_acceptance__creator=request.user
    )

    serializer = DeliverableSerializer(deliverables, many=True)
    return Response(serializer.data, status=200)
