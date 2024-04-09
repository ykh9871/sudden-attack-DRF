from datetime import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserSerializer, UserInfoSerializer


class SignupView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 이름"
                ),
                "nickname": openapi.Schema(
                    type=openapi.TYPE_STRING, description="닉네임"
                ),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
                "occupation": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="직업 ID"
                ),
            },
            required=["username", "nickname", "email", "password", "occupation"],
        ),
        responses={201: "User registered successfully"},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
            required=["email", "password"],
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            401: "Incorrect email or password",
        },
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = TokenObtainPairSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Incorrect email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserInfoSerializer},
    )
    def get(self, request):
        user_info = User.objects.filter(email=request.user.email).first()
        if user_info:
            serializer = UserInfoSerializer(user_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 이름"
                ),
                "nickname": openapi.Schema(
                    type=openapi.TYPE_STRING, description="닉네임"
                ),
                "occupation": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="직업 ID"
                ),
            },
            required=["username", "nickname", "occupation"],
        ),
        responses={200: "User information updated successfully"},
    )
    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user:
                user.username = serializer.validated_data["username"]
                user.nickname = serializer.validated_data["nickname"]
                user.occupation = serializer.validated_data["occupation"]
                user.save()
                return Response(
                    {"message": "User information updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "current_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="현재 비밀번호"
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="새로운 비밀번호"
                ),
            },
            required=["current_password", "new_password"],
        ),
        responses={
            200: "User password updated successfully",
            401: "Incorrect current password",
        },
    )
    def put(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        user = authenticate(email=request.user.email, password=current_password)
        if user:
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "User password updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Incorrect current password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class WithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
            required=["password"],
        ),
        responses={200: "User account deleted successfully", 401: "Incorrect password"},
    )
    def delete(self, request):
        password = request.data.get("password")
        user = authenticate(email=request.user.email, password=password)
        if user:
            user.active = False
            user.deleted_at = timezone.now()
            user.save()
            return Response(
                {"message": "User account deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED
            )
