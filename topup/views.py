from datetime import timedelta, datetime, date
import csv

from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Sum
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import PaymentTransaction, TopUpOrder
from .serializers import TopUpOrderSerializer, RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class TopUpAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            transaction = PaymentTransaction.objects.get(topup_order=order)
            return Response({
                "message": "Top-up order created successfully.",
                "transaction_id": transaction.transaction_id,
                "status": order.status
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentWebhookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        status_update = request.data.get('status')

        try:
            transaction = PaymentTransaction.objects.get(transaction_id=transaction_id)
        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        transaction.status = status_update
        transaction.save()

        return Response({"message": "Transaction and order status updated."}, status=200)



@method_decorator(staff_member_required, name='dispatch')
class TopUpDashboardView(TemplateView):
    template_name = "topup/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                start_date = now.date() - timedelta(days=30)
                end_date = now.date()
        else:
            start_date = now.date() - timedelta(days=30)
            end_date = now.date()

        # Successful orders in date range
        filtered_orders = TopUpOrder.objects.filter(
            status='success',
            created_at__date__range=[start_date, end_date]
        )

        # Daily Revenue for Chart
        daily_revenue = (
            filtered_orders
            .values('created_at__date')
            .annotate(total_revenue=Sum('product__price'))
            .order_by('created_at__date')
        )

        # Game-wise Revenue
        game_revenue = (
            filtered_orders
            .values('product__game__name')
            .annotate(total=Sum('product__price'))
            .order_by('-total')
        )

        # Most Active Users
        active_users = (
            TopUpOrder.objects
            .filter(created_at__date__range=[start_date, end_date])
            .values('user_email')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )

        # Top 5 Most Purchased Products (globally)
        top_products = (
            TopUpOrder.objects
            .filter(status='success')
            .values('product__name')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

        # Failed orders this month
        start_of_month = now.replace(day=1)
        failed_count = (
            TopUpOrder.objects
            .filter(status='failed', created_at__gte=start_of_month)
            .count()
        )

        context.update({
            'daily_revenue': daily_revenue,
            'game_revenue': game_revenue,
            'active_users': active_users,
            'start_date': start_date,
            'end_date': end_date,
            'top_products': top_products,
            'failed_count': failed_count,
            'today_date': date.today().isoformat(),
        })

        return context



class ExportOrdersCSV(APIView):
    def get(self, request):
        orders = TopUpOrder.objects.select_related('product').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_orders.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'User Email', 'Product', 'Game', 'Price', 'Status', 'Created At'])
        for order in orders:
            writer.writerow([
                order.id,
                order.user_email,
                order.product.name,
                order.product.game.name,
                order.product.price,
                order.status,
                order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        return response


class ExportFailedPaymentsCSV(APIView):
    def get(self, request):
        failed = TopUpOrder.objects.select_related('product').filter(status='failed')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="failed_payments.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'User Email', 'Product', 'Game', 'Price', 'Status', 'Created At'])
        for order in failed:
            writer.writerow([
                order.id,
                order.user_email,
                order.product.name,
                order.product.game.name,
                order.product.price,
                order.status,
                order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        return response
