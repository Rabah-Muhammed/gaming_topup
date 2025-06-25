from django.urls import path
from .views import (
    TopUpAPIView,
    TopUpDashboardView,
    RegisterView,
    PaymentWebhookView,
    ExportOrdersCSV,
    ExportFailedPaymentsCSV
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup-api'),
    path('dashboard/', TopUpDashboardView.as_view(), name='topup-dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment/webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
    path('export/orders/', ExportOrdersCSV.as_view(), name='export-orders'),
    path('export/failures/', ExportFailedPaymentsCSV.as_view(), name='export-failures'),
]  