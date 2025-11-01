from django.urls import path
from .views import (
    OrderCreateAPIView,
    OrderRetrieveAPIView,
    OrderListAPIView,
    OrderSellerStatusUpdateAPIView,
    OrderBuyerStatusUpdateAPIView,
)

app_name = 'transaction'

urlpatterns = [
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/<int:id>/', OrderRetrieveAPIView.as_view(), name='order-retrieve'),
    path('orders/<int:id>/status/seller/', OrderSellerStatusUpdateAPIView.as_view(), name='order-status-update-seller'),
    path('orders/<int:id>/status/buyer/', OrderBuyerStatusUpdateAPIView.as_view(), name='order-status-update-buyer'),
]
