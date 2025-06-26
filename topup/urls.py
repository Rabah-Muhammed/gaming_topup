from django.urls import path
from .views import (
    RegisterView,
    UserProfileView,
    TopUpAPIView,
    TopUpDashboardView,
    PaymentWebhookView,
    ExportOrdersCSV,
    ExportFailedPaymentsCSV
    
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('topup/', TopUpAPIView.as_view(), name='topup-api'),
    path('payment/webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
    path('dashboard/', TopUpDashboardView.as_view(), name='topup-dashboard'),
    path('export/orders/', ExportOrdersCSV.as_view(), name='export-orders'),
    path('export/failures/', ExportFailedPaymentsCSV.as_view(), name='export-failures'),
]  