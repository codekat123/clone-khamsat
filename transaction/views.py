from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Order, OrderStatusHistory
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from user_profile.permissions import IsBuyer, IsSeller
from services.models import Service



class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBuyer]

    def perform_create(self, serializer):
        buyer = getattr(self.request.user, 'buyer_profile', None)
        slug = self.kwargs.get('slug')
        service = get_object_or_404(Service, slug=slug)

        if buyer is None:
            raise ValidationError({"detail": "Buyer profile not found."})

        if service.seller == buyer:
            raise ValidationError({"detail": "You cannot order your own service."})

        serializer.save(
            buyer=buyer,
            service=service,
            seller=service.seller
        )



class OrderRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,IsSeller]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(seller__user=user)



class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Order.objects.filter(seller__user=self.request.user)



class OrderSellerStatusUpdateAPIView(UpdateAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Order.objects.filter(seller__user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        user = self.request.user

        allowed_statuses = [
            Order.Status.PENDING,
            Order.Status.REJECTED,
            Order.Status.IN_PROGRESS,
        ]

        if new_status not in allowed_statuses:
            raise ValidationError("Sellers can only set orders to pending, rejected, or in progress.")

        serializer.save()

        OrderStatusHistory.objects.create(
            order=instance,
            user=user,
            old_status=old_status,
            new_status=new_status,
        )



class OrderBuyerStatusUpdateAPIView(UpdateAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsBuyer]

    def get_queryset(self):
        return Order.objects.filter(buyer__user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        user = self.request.user

        allowed_statuses = [
            Order.Status.CANCELLED,
            Order.Status.COMPLETED,
        ]

        if new_status not in allowed_statuses:
            raise ValidationError("Buyers can only cancel or mark orders as completed.")

        serializer.save()

        OrderStatusHistory.objects.create(
            order=instance,
            user=user,
            old_status=old_status,
            new_status=new_status,
        )
