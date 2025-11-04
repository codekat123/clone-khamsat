from django.core.cache import cache
from django.db.models import Count, Avg, Max
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from services.models import Service
from services.serializers import ServiceSerializer
from user_profile.permissions import IsAdmin
from user_profile.models import SellerProfile, BuyerProfile
from transaction.models import Order
from wallet.models import Wallet
import logging


logger = logging.getLogger("admin_access")


# ---------------------- Base Service Views ---------------------- #

class BaseServiceListAPIView(ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self, *, is_active=True, cache_key=None):
        if not cache_key:
            raise ValueError("cache_key is required")

        services = cache.get(cache_key)
        if services is None:
            services = (
                Service.objects
                .select_related('seller', 'seller__user')
                .filter(is_active=is_active)
            )
            cache.set(cache_key, list(services), timeout=86400)
        return services


class ActiveServiceAPIView(BaseServiceListAPIView):
    def get_queryset(self):
        return super().get_queryset(is_active=True, cache_key='active_services')


class InactiveServiceAPIView(BaseServiceListAPIView):
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return super().get_queryset(is_active=False, cache_key='inactive_services')


class ActivateServiceAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        slug = request.data.get('slug')
        if not slug:
            raise ValidationError({"slug": "This field is required."})

        service = get_object_or_404(Service, slug=slug)
        if service.is_active:
            return Response(
                {"message": "Service is already active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service.is_active = True
        service.save(update_fields=["is_active"])

        cache.delete_many(['inactive_services', 'active_services'])

        return Response(
            {"message": f"Service '{service.title}' has been activated successfully."},
            status=status.HTTP_200_OK
        )


# ---------------------- Utility ---------------------- #

def mask_email(email):
    if not email or "@" not in email:
        return None
    local, domain = email.split("@", 1)
    return f"{local[:1]}***{local[-1:]}@{domain}"


# ---------------------- Seller Info ---------------------- #

class AboutSeller(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, seller_id):
        seller = get_object_or_404(
            SellerProfile.objects.select_related('user'),
            id=seller_id
        )

        summary = (
            SellerProfile.objects.filter(id=seller_id)
            .annotate(
                orders_count=Count('orders', distinct=True),
                unique_buyers=Count('orders__buyer', distinct=True),
                avg_rating=Avg('ratings__stars'),
                last_order=Max('orders__created_at'),
            )
            .values('orders_count', 'unique_buyers', 'avg_rating', 'last_order')
            .first()
        ) or {}

        recent_orders = list(
            Order.objects.filter(seller=seller)
            .select_related('buyer__user')
            .only('id', 'price', 'created_at',
                  'buyer__id', 'buyer__user__first_name', 'buyer__user__last_name')
            .order_by('-created_at')[:5]
            .values('id', 'price', 'created_at',
                    'buyer__id', 'buyer__user__first_name', 'buyer__user__last_name')
        )

        for o in recent_orders:
            o['buyer'] = f"{o.pop('buyer__user__first_name', '')} {o.pop('buyer__user__last_name', '')}".strip() or None

        wallet_balance = getattr(getattr(seller.user, 'wallet', None), 'balance_cents', None)

        logger.info("admin_access", extra={
            "admin_id": request.user.id,
            "admin_username": request.user.username,
            "action": "view_seller_summary",
            "seller_id": seller_id,
            "timestamp": timezone.now().isoformat(),
            "ip": request.META.get('REMOTE_ADDR')
        })

        return Response({
            "seller_id": seller.id,
            "seller_name": seller.user.get_full_name(),
            "summary": summary,
            "recent_orders": recent_orders,
            "wallet_balance": wallet_balance,
        })


# ---------------------- Buyer Info ---------------------- #

class AboutBuyer(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, buyer_id):
        buyer = get_object_or_404(
            BuyerProfile.objects.select_related('user'),
            id=buyer_id
        )

        summary = (
            BuyerProfile.objects.filter(id=buyer.id)
            .annotate(
                orders_count=Count('orders', distinct=True),
                unique_sellers=Count('orders__seller', distinct=True),
                last_order=Max('orders__created_at')
            )
            .values('orders_count', 'unique_sellers', 'last_order')
            .first()
        ) or {}

        recent_orders = list(
            Order.objects.filter(buyer=buyer)
            .select_related('seller__user')
            .only('id', 'price', 'created_at',
                  'seller__id', 'seller__user__first_name', 'seller__user__last_name')
            .order_by('-created_at')[:5]
            .values('id', 'price', 'created_at',
                    'seller__id', 'seller__user__first_name', 'seller__user__last_name')
        )

        for o in recent_orders:
            o['seller'] = f"{o.pop('seller__user__first_name', '')} {o.pop('seller__user__last_name', '')}".strip() or None

        wallet_balance = getattr(getattr(buyer.user, 'wallet', None), 'balance_cents', None)

        logger.info("admin_access", extra={
            "admin_id": request.user.id,
            "admin_username": request.user.username,
            "action": "view_buyer_summary",
            "buyer_id": buyer_id,
            "timestamp": timezone.now().isoformat(),
            "ip": request.META.get('REMOTE_ADDR')
        })

        return Response({
            "buyer_id": buyer.id,
            "buyer_name": buyer.user.get_full_name(),
            "summary": summary,
            "recent_orders": recent_orders,
            "wallet_balance": wallet_balance,
        })

