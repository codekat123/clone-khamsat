from django.urls import path
from .views import (
     ActiveServiceAPIView,
     InactiveServiceAPIView,
     ActivateServiceAPIView,
     AboutSeller,
     AboutBuyer,
)


app_name = "admin"


urlpatterns = [
     path('list/activated/service/',ActiveServiceAPIView.as_view(),name='activated-service-list'),
     path('list/inactivated/service/',InactiveServiceAPIView.as_view(),name='inactivated-service-list'),
     path('inactivate/service/',ActivateServiceAPIView.as_view(),name='activate-service'),
     path('about/seller/<sell_id>/',AboutSeller.as_view(),name='about-seller'),
     path('about/buyer/<buyer_id>/',AboutBuyer.as_view(),name='about-Buyer'),
]