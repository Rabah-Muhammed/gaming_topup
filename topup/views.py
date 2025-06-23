from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TopUpOrderSerializer
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from datetime import timedelta
from django.utils import timezone
from .models import TopUpOrder

class TopUpAPIView(APIView):
    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Top-up order created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(staff_member_required, name='dispatch')
class TopUpDashboardView(TemplateView):
    template_name = "topup/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # Top 5 Most Purchased Products
        top_products = (
            TopUpOrder.objects
            .filter(status='success')
            .values('product__name')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

        # Daily Revenue for Last 7 Days
        last_7_days = now - timedelta(days=6)
        daily_revenue = (
            TopUpOrder.objects
            .filter(status='success', created_at__date__gte=last_7_days.date())
            .values('created_at__date')
            .annotate(total_revenue=Sum('product__price'))
            .order_by('created_at__date')
        )

        # Failed Payment Count (Current Month)
        start_of_month = now.replace(day=1)
        failed_count = (
            TopUpOrder.objects
            .filter(status='failed', created_at__gte=start_of_month)
            .count()
        )

        # Chart data
        top_products_labels = [item['product__name'] for item in top_products]
        top_products_data = [item['total'] for item in top_products]

        revenue_dates = [item['created_at__date'].strftime('%Y-%m-%d') for item in daily_revenue]
        revenue_values = [float(item['total_revenue']) for item in daily_revenue]

        # Add everything to context
        context.update({
            'top_products': top_products,
            'daily_revenue': daily_revenue,
            'failed_count': failed_count,
            'top_products_labels': top_products_labels,
            'top_products_data': top_products_data,
            'revenue_dates': revenue_dates,
            'revenue_values': revenue_values,
        })

        return context