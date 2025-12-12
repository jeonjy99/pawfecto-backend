from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, BrandSerializer, CreatorSerializer, StyleTagSerializer

User = get_user_model()


# ============================================
# 1) 회원가입
# ============================================
@api_view(['POST'])
def signup(request):

    account_type = request.data.get("account_type")

    if account_type == "brand":
        serializer = BrandSerializer(data=request.data)
    elif account_type == "creator":
        serializer = CreatorSerializer(data=request.data)
    else:
        return Response({"error": "Invalid account_type"}, status=400)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "signup success", "user": UserSerializer(user).data},
            status=201
        )

    return Response(serializer.errors, status=400)

# ============================================
# 2) 로그인
# ============================================
@api_view(['POST'])
def login_view(request):

    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")

        # 값이 비어있는지 확인
        if not username or not password:
            return Response(
                {"error": "username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        # 브랜드/크리에이터 구분 직렬화
        if user.account_type == "brand":
            data = BrandSerializer(user).data
        else:
            data = CreatorSerializer(user).data

        return Response(
            {"message": "login success", "user": data},
            status=status.HTTP_200_OK
        )

# ============================================
# 3) 로그아웃
# ============================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        return Response({"message": "logout success"}, status=status.HTTP_200_OK)


# ============================================
# 4) 내 정보 조회
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=200)


# ============================================
# 5) 브랜드 프로필 조회
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brand_profile(request, brand_id):
    user = get_object_or_404(User, id=brand_id, account_type="brand")
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


# ============================================
# 6) 크리에이터 프로필 조회
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def creator_profile(request, creator_id):
    qs = User.objects.filter(id=creator_id, account_type="creator")
    if not qs.exists():
        return Response({"error": "Creator not found"}, status=404)
    serializer = UserSerializer(qs.first())
    return Response(serializer.data, status=200)


# ============================================
# 7) 프로필 수정 (PUT)
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data.copy()
    data.pop("account_type", None)  # 계정 타입 변경 방지

    serializer = UserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "profile updated", "user": serializer.data},
            status=200
        )
    return Response(serializer.errors, status=400)


# ============================================
# 8) 크리에이터 스타일 태그 수정
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_style_tags(request, creator_id):

    if request.user.id != creator_id:
        return Response({"error": "본인만 수정할 수 있습니다."}, status=403)

    user = get_object_or_404(User, id=creator_id, account_type="creator")

    style_tag_ids = request.data.get("style_tags", [])

    if not isinstance(style_tag_ids, list):
        return Response(
            {"error": "style_tags must be a list of IDs"},
            status=400
        )

    user.style_tags.set(style_tag_ids)

    return Response(
        {
            "message": "style tags updated",
            "style_tags": StyleTagSerializer(user.style_tags.all(), many=True).data
        },
        status=200
    )


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import get_user_model

# # from .models import User
# from .serializers import UserSerializer

# User = get_user_model()
# # Create your views here.

# @api_view(['GET'])
# def user_list(request):
#     if request.method == "GET":
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)