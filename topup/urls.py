from django.urls import path
from .views import TopUpAPIView,TopUpDashboardView

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup-api'),
    path('dashboard/', TopUpDashboardView.as_view(), name='topup-dashboard'),
]
