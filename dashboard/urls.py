from django.urls import path
from .views import (
     ToggleServiceStatusAPIView,
     SellerInfoAPIView
)


app_name = 'dashboard'

urlpatterns = [
     path('toggle/service/status/<slug:slug>/',ToggleServiceStatusAPIView.as_view(),name='toggle-service'),
     path('get-seller-info/',SellerInfoAPIView.as_view(),name='get-seller-info')
]