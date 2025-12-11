from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [

    # 회원가입
    path('signup/', views.signup, name='signup'),

    # JWT 로그인 / 리프레시 토큰
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 내 정보
    path('me/', views.me, name='me'),

    # 프로필 업데이트
    path('update-profile/', views.update_profile, name='update-profile'),

    # 브랜드 / 크리에이터 프로필 조회
    path('brand/<int:brand_id>/', views.brand_profile, name='brand-profile'),
    path('creator/<int:creator_id>/', views.creator_profile, name='creator-profile'),

    # 크리에이터 스타일 태그 업데이트
    path('creator/<int:creator_id>/style-tags/', views.update_style_tags, name='update-style-tags'),
]
