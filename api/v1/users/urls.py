from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserCreateView, UserDetailView

urlpatterns = [
    path('', UserCreateView.as_view()),
    path('/me', UserDetailView.as_view()),
    path('/login', TokenObtainPairView.as_view()),
    path('/login/refresh', TokenRefreshView.as_view()),
]
