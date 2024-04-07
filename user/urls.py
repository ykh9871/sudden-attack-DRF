from django.urls import path
from .views import (
    SignupView,
    LoginView,
    UserInfoView,
    UpdatePasswordView,
    WithdrawalView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("info/", UserInfoView.as_view(), name="user-info"),
    path("password/", UpdatePasswordView.as_view(), name="update-password"),
    path("withdrawal/", WithdrawalView.as_view(), name="withdrawal"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
