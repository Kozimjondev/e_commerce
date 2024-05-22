from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginAPIView, LogoutAPIView, ChangePasswordView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change-password/<uuid:guid>/', ChangePasswordView.as_view(), name='change_password'),
]
