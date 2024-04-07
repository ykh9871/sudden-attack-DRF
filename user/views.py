from datetime import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, UserInfoSerializer


class SignupView(APIView):
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
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user.refresh_token = str(refresh)
            user.save()
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "token_type": "bearer",
                    "nickname": user.nickname,
                    "refresh_token": str(refresh),
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

    def get(self, request):
        user_info = User.objects.filter(email=request.user.email).first()
        if user_info:
            serializer = UserInfoSerializer(user_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user:
                user.username = serializer.validated_data["username"]
                user.nickname = serializer.validated_data["nickname"]
                user.occupation.name = serializer.validated_data["occupation_name"]
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
