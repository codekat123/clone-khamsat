from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from services.models import Service
from user_profile.permissions import IsSeller
from wallet.models import Wallet,WalletTransaction
from transaction.models import Order
from django.db.models import Sum, Count,Avg,F, ExpressionWrapper, fields
from datetime import datetime, timedelta
from rating.models import Rating
from django.utils import timezone
from .serializers import SellerDashboardSerializer
from django.core.cache import cache

class ToggleServiceStatusAPIView(APIView):
    permission_classes = [IsSeller]

    def post(self, request):
        slug = request.data.get('slug')

        if not slug:
            raise ValidationError('You must provide a service slug.')

        service = get_object_or_404(Service, slug=slug)


        if service.freelancer != request.user.seller_profile:
            raise PermissionDenied("You don't have permission to modify this service.")


        service.is_pause = not service.is_pause
        service.save()

        status_msg = (
            "Your service is now hidden (paused)."
            if service.is_pause
            else "Your service is now visible to buyers."
        )

        return Response(
            {"message": status_msg, "is_active": service.is_active},
            status=status.HTTP_200_OK
        )



class SellerInfoAPIView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        user = request.user
        seller = user.seller_profile
        cache_key = f"seller_dashboard_{user.id}"

        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        wallet = get_object_or_404(Wallet, user=user)

        
        services_count = Service.objects.filter(freelancer=seller).count()

        orders = Order.objects.filter(seller=seller).select_related('buyer')
        active_orders_count = orders.filter(status=Order.Status.IN_PROGRESS).count()

        completed_orders = orders.filter(status=Order.Status.COMPLETED)
        total_earnings = completed_orders.aggregate(total=Sum('price'))['total'] or 0

        
        total_orders = orders.count()
        completed_count = completed_orders.count()
        completion_rate = round(
            (completed_count / total_orders * 100) if total_orders else 0, 2
        )

        
        top_service = (
            Service.objects.filter(freelancer=seller)
            .annotate(order_count=Count('orders'))
            .order_by('-order_count')
            .first()
        )

        
        now = timezone.now()
        current_month = now.month
        monthly_earnings = (
            completed_orders.filter(created_at__month=current_month)
            .aggregate(total=Sum('price'))['total']
            or 0
        )

        
        last_month = (now - timedelta(days=30)).month
        last_month_earnings = (
            completed_orders.filter(created_at__month=last_month)
            .aggregate(total=Sum('price'))['total']
            or 0
        )
        growth_rate = round(
            ((monthly_earnings - last_month_earnings) / last_month_earnings * 100)
            if last_month_earnings
            else 0,
            2,
        )

       
        order_status_summary = (
            orders.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        
        recent_transactions = list(
            WalletTransaction.objects.filter(wallet=wallet)
            .order_by('-created_at')[:5]
            .values('id', 'amount', 'transaction_type', 'created_at')
        )

        # Average rating
        services_id = Service.objects.filter(freelancer=seller).values_list('id', flat=True)
        average_rating = (
            Rating.objects.filter(service__in=services_id)
            .aggregate(
                average_rate_all_services=Avg('stars'),
                total_ratings=Count('id'),
            )
        )

        
        how_many_days_left = list(
            orders.filter(status=Order.Status.IN_PROGRESS)
            .annotate(
                days_left=ExpressionWrapper(
                    F('deadline') - timezone.now().date(),
                    output_field=fields.DurationField(),
                )
            )
            .values('id', 'buyer', 'days_left')
        )

        
        data = {
            "wallet_balance": wallet.balance_cents,
            "services_count": services_count,
            "active_orders_count": active_orders_count,
            "total_earnings": total_earnings,
            "monthly_earnings": monthly_earnings,
            "growth_rate": growth_rate,
            "completion_rate": completion_rate,
            "top_service": top_service.title if top_service else None,
            "recent_transactions": recent_transactions,
            "average_rating": average_rating,
            "active_orders_deadlines": how_many_days_left,
            "order_status_summary": list(order_status_summary),
        }

        
        cache.set(cache_key, data, timeout=60*60)

        return Response(SellerDashboardSerializer(data).data, status=status.HTTP_200_OK)