from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Campaign, CampaignAcceptance, Deliverable
from accounts.models import User
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignAcceptanceSerializer,
    DeliverableSerializer
)


# -----------------------------------------------------------
# 1. 캠페인 생성 (GET / POST)
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
# 2. 캠페인 상세 조회 + 수정 (GET / PUT)
# -----------------------------------------------------------
@api_view(['GET', 'PUT'])
def campaign_detail(request, id):
    campaign = get_object_or_404(Campaign, pk=id)

    # GET - 상세 조회
    if request.method == 'GET':
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data, status=200)

    # PUT - 수정
    if request.method == 'PUT':
        if request.user != campaign.brand:
            return Response({"error": "수정 권한 없음"}, status=403)

        serializer = CampaignSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)



# -----------------------------------------------------------
# 3. 브랜드 캠페인 목록
# -----------------------------------------------------------
@api_view(['GET'])
def brand_campaigns(request, brand_id):

    all_campaigns = Campaign.objects.all()
    brand_campaign_list = []

    for camp in all_campaigns:
        if camp.brand_id == brand_id:
            brand_campaign_list.append(camp)

    serializer = CampaignListSerializer(brand_campaign_list, many=True)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 4. 크리에이터가 받은 오퍼 목록 (pending 상태)
# -----------------------------------------------------------
@api_view(['GET'])
def creator_offers(request, creator_id):

    if request.method == 'GET':
        offers = CampaignAcceptance.objects.filter(creator_id=creator_id)

        serializer = CampaignAcceptanceSerializer(offers, many=True)
        return Response(serializer.data, status=200)


# -----------------------------------------------------------
# 5. 크리에이터가 진행중인 캠페인 목록 (accepted 상태)
# -----------------------------------------------------------
@api_view(['GET'])
def creator_progress(request, creator_id):

    all_acc = CampaignAcceptance.objects.all()
    progressing = []

    for acc in all_acc:
        if acc.creator_id == creator_id and acc.acceptance_status == 'accepted':
            progressing.append(acc)

    serializer = CampaignAcceptanceSerializer(progressing, many=True)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 6. 추천 크리에이터 조회
# -----------------------------------------------------------
@api_view(['GET'])
def recommend_creators(request, id):

    campaign = get_object_or_404(Campaign, pk=id)
    target_type = campaign.target_pet_type
    min_followers = campaign.min_follower_count

    creators = User.objects.all()
    recommended = []

    for c in creators:
        if c.account_type != "creator":
            continue

        if c.follower_count is None:
            continue

        # 조건 직접 검사
        if c.follower_count >= min_followers:
            if target_type is None or c.pet_type == target_type:
                recommended.append(c)

    from accounts.serializers import CreatorSerializer
    serializer = CreatorSerializer(recommended, many=True)

    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 7. 브랜드가 크리에이터에게 초대 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def invite_creator(request, id):

    campaign = get_object_or_404(Campaign, pk=id)
    creator_id = request.data.get("creator_id")

    creator = get_object_or_404(User, pk=creator_id)

    acceptance = CampaignAcceptance.objects.create(
        creator=creator,
        campaign=campaign,
        acceptance_status="pending",
        applied_at=timezone.now()
    )

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response(serializer.data, status=201)



# -----------------------------------------------------------
# 8. 크리에이터 캠페인 수락 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def accept_campaign(request, id):

    acceptance = None

    for acc in CampaignAcceptance.objects.all():
        if acc.campaign_id == id and acc.creator == request.user:
            acceptance = acc
            break

    if acceptance is None:
        return Response({"error": "오퍼 없음"}, status=404)

    acceptance.acceptance_status = "accepted"
    acceptance.accepted_at = timezone.now()
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 9. 크리에이터 캠페인 거절 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def reject_campaign(request, id):

    acceptance = None

    for acc in CampaignAcceptance.objects.all():
        if acc.campaign_id == id and acc.creator == request.user:
            acceptance = acc
            break

    if acceptance is None:
        return Response({"error": "오퍼 없음"}, status=404)

    acceptance.acceptance_status = "rejected"
    acceptance.save()

    serializer = CampaignAcceptanceSerializer(acceptance)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 10. 딜리버러블 제출 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def submit_deliverable(request, id):

    acceptance = None
    for acc in CampaignAcceptance.objects.all():
        if acc.campaign_id == id and acc.creator == request.user:
            acceptance = acc
            break

    if acceptance is None:
        return Response({"error": "참여한 캠페인 아님"}, status=404)

    Deliverable.objects.create(
        campaign_acceptance=acceptance,
        posted_at=timezone.now(),
        post_url=request.data.get("post_url"),
        deliverable_status="incomplete"
    )

    return Response({"message": "딜리버러블 제출 완료"}, status=201)



# -----------------------------------------------------------
# 11. 딜리버러블 조회 (GET)
# -----------------------------------------------------------
@api_view(['GET'])
def get_deliverables(request, id):

    delv_list = []
    all_delv = Deliverable.objects.all()

    for d in all_delv:
        if d.campaign_acceptance.campaign_id == id:
            delv_list.append(d)

    serializer = DeliverableSerializer(delv_list, many=True)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 12. 딜리버러블 승인 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def approve_deliverable(request, id):

    deliverable = get_object_or_404(Deliverable, pk=id)
    deliverable.deliverable_status = "completed"
    deliverable.save()

    serializer = DeliverableSerializer(deliverable)
    return Response(serializer.data, status=200)



# -----------------------------------------------------------
# 13. 딜리버러블 수정 요청 (POST)
# -----------------------------------------------------------
@api_view(['POST'])
def request_changes(request, id):

    deliverable = get_object_or_404(Deliverable, pk=id)
    deliverable.deliverable_status = "incomplete"
    deliverable.save()

    return Response({"message": "수정 요청 완료"}, status=200)



# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import render
# from .models import Campaign, CampaignAcceptance, Deliverable
# from .serializers import CampaignListSerializer, CampaignSerializer, CampaignAcceptanceSerializer, DeliverableSerializer

# # Create your views here.
# # @api_view(['GET'])
# # def brand_list(request):
# #     if request.method == 'GET':
# #         brand = AccountBrand.objects.all()
# #         serializer = AccountBrandSerializer(brand, many=True)
# #         return Response(serializer.data)

# # def index(request):

# #     return render(request, 'myapp/index.html')


# @api_view(['GET', 'POST'])
# def campaign_list(request):
#     if request.method == "GET":
#         campaigns = Campaign.objects.all()
#         serializer = CampaignListSerializer(campaigns, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         print(request.data)
#         serializer = CampaignSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data)
#             return Response(serializer.data)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
