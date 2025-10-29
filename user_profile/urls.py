from django.urls import path
from .views import *

app_name = 'profile'


urlpatterns = [
    path('profile/seller/', SellerProfileAPIView.as_view(), name='my-seller-profile'),
    path('profile/seller/<str:username>/', SellerProfileAPIView.as_view(), name='seller-profile-detail'),

    path('profile/buyer/', BuyerProfileAPIView.as_view(), name='my-buyer-profile'),
    path('profile/buyer/<str:username>/', BuyerProfileAPIView.as_view(), name='buyer-profile-detail'),
]