from django.urls import path
from .views import StaffAPIView, StaffDetailAPIView, StaffCreateAPIView, StaffDeleteAPIView, StaffUpdateAPIView

urlpatterns = [
    path('list/', StaffAPIView.as_view(), name='staff-list'),
    path('-create/', StaffCreateAPIView.as_view(), name='staff-create'),
    path('-detail/<uuid:guid>/', StaffDetailAPIView.as_view(), name='staff-detail'),
    path('-update/<uuid:guid>/', StaffUpdateAPIView.as_view(), name='staff-detail'),
    path('-delete/<uuid:guid>/', StaffDeleteAPIView.as_view(), name='staff-detail'),
]
