from django.urls import path
from .views import (
     RatingListCreateAPIView,
     RatingDetailAPIView,
     get_average_rating_of_service,
)

app_name = 'rating'

urlpatterns = [
    path('services/<slug:slug>/ratings/', RatingListCreateAPIView.as_view(), name='rating-list-create'),
    path('services/<slug:slug>/ratings/<int:id>/', RatingDetailAPIView.as_view(), name='rating-detail'),
    path('service/average/<slug:slug>/rating/',get_average_rating_of_service,name='average'),
]