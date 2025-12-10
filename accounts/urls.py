from django.urls import path
from . import views

urlpatterns = [

    # 회원가입 / 로그인 / 로그아웃
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

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


# from django.urls import path
# from . import views


# app_name = 'accounts'
# urlpatterns = [
#     path('user', views.user_list, name='user_list'),
# ]