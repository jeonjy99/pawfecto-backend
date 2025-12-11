from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [

    # =====================================================
    # 브랜드 기능
    # =====================================================

    # 1) 브랜드 캠페인 목록 조회
    path(
        'brand/<int:brand_id>/campaigns/',
        views.brand_campaign_list,
        name='brand_campaign_list'
    ),

    # 2) 캠페인 생성
    path(
        'campaign/create/',
        views.create_campaign,
        name='create_campaign'
    ),

    # 3) 캠페인 상세 조회
    path(
        'campaign/<int:campaign_id>/',
        views.campaign_detail,
        name='campaign_detail'
    ),

    # 4) 캠페인 수정
    path(
        'campaign/<int:campaign_id>/update/',
        views.update_campaign,
        name='update_campaign'
    ),

    # 5) 특정 캠페인의 오퍼(신청) 목록 조회
    path(
        'campaign/<int:campaign_id>/acceptances/',
        views.campaign_acceptance_list,
        name='campaign_acceptance_list'
    ),

    # 6) 캠페인 진행 상황 조회 (Deliverable)
    path(
        'campaign/<int:campaign_id>/progress/',
        views.campaign_progress,
        name='campaign_progress'
    ),


    # =====================================================
    # 크리에이터 기능
    # =====================================================

    # 7) 크리에이터 오퍼 조회
    path(
        'creator/<int:creator_id>/offers/',
        views.creator_campaign_offers,
        name='creator_campaign_offers'
    ),

    # 8) 수락
    path(
        'creator/campaign/<int:campaign_id>/accept/',
        views.accept_campaign,
        name='accept_campaign'
    ),

    # 9) 거절
    path(
        'creator/campaign/<int:campaign_id>/reject/',
        views.reject_campaign,
        name='reject_campaign'
    ),

    # 10) 진행상황 조회 (크리에이터 관점)
    path(
        'creator/<int:creator_id>/progress/',
        views.creator_progress,
        name='creator_progress'
    ),
]

