from django.urls import path
from . import views

urlpatterns = [

<<<<<<< HEAD
    # -----------------------------------------------------------
    # 캠페인 관련
    # -----------------------------------------------------------
    path('campaigns/create/', views.create_campaign, name='create_campaign'),

    path('campaigns/<int:id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:id>/update/', views.campaign_detail, name='update_campaign'),

    path('brands/<int:brand_id>/campaigns/', views.brand_campaigns, name='brand_campaigns'),

    path('creators/<int:creator_id>/offers/', views.creator_offers, name='creator_offers'),
    path('creators/<int:creator_id>/progress/', views.creator_progress, name='creator_progress'),


    # -----------------------------------------------------------
    # 크리에이터 추천 기능
    # -----------------------------------------------------------
    path('campaigns/<int:id>/recommendations/', views.recommend_creators, name='recommend_creators'),


    # -----------------------------------------------------------
    # 캠페인 신청 / 초대 / 수락
    # -----------------------------------------------------------
    path('campaigns/<int:id>/invite/', views.invite_creator, name='invite_creator'),
    path('campaigns/<int:id>/accept/', views.accept_campaign, name='accept_campaign'),
    path('campaigns/<int:id>/reject/', views.reject_campaign, name='reject_campaign'),


    # -----------------------------------------------------------
    # 딜리버러블 제출 / 조회 / 승인 / 수정요청
    # -----------------------------------------------------------
    path('campaigns/<int:id>/deliverables/submit/', views.submit_deliverable, name='submit_deliverable'),
    path('campaigns/<int:id>/deliverables/', views.get_deliverables, name='get_deliverables'),

    path('deliverables/<int:id>/approve/', views.approve_deliverable, name='approve_deliverable'),
    path('deliverables/<int:id>/request-changes/', views.request_changes, name='request_changes'),
]
=======
    # 캠페인 생성 / 조회 / 수정 / 삭제
    path('campaigns/create/', views.create_campaign, name='create_campaign'),
    path('campaigns/<int:id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:id>/update/', views.update_campaign, name='update_campaign'),
    path('campaigns/<int:id>/delete/', views.delete_campaign, name='delete_campaign'),

    # 브랜드별 캠페인 목록
    path('brands/<int:brand_id>/campaigns/', views.brand_campaigns, name='brand_campaigns'),

    # 크리에이터 오퍼 목록
    path('creators/<int:creator_id>/offers/', views.creator_offers, name='creator_offers'),

    # 크리에이터 진행중 캠페인 목록
    path('creators/<int:creator_id>/progress/', views.creator_progress, name='creator_progress'),

    # 캠페인 기반 크리에이터 추천
    path('campaigns/<int:id>/recommendations/', views.recommend_creators, name='recommend_creators'),

    # 신규: 신청/수락/거절 기능
    path('campaigns/<int:id>/invite/', views.invite_creator, name='invite_creator'),
    path('campaigns/<int:id>/accept/', views.accept_campaign, name='accept_campaign'),
    path('campaigns/<int:id>/reject/', views.reject_campaign, name='reject_campaign'),
]
>>>>>>> main
