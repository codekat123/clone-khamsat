from django.urls import path
from .views import (
     ToggleServiceStatusAPIView
)


app_name = 'dashboard'

urlpatterns = [
     path('toggle/service/status/<slug:slug>/',ToggleServiceStatusAPIView.as_view(),name='toggle-service'),
]