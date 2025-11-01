from django.urls import path
from .views import *

app_name = 'services'

urlpatterns = [
    path('<slug:slug>/services/', ServiceListAPIView.as_view(), name='service-list'),
    path('service/seller/',ServiceSellerListAPIView.as_view,name='service-seller'),
    path('<slug:slug>/services/create/', ServiceCreateAPIView.as_view(), name='service-create'),
    path('<slug:slug>/update/', ServiceUpdateAPIView.as_view(), name='service-update'),
    path('<slug:slug>/delete/', ServiceDeleteAPIView.as_view(), name='service-delete'),
    path('<slug:slug>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('category/',CategoryCreateListAPIView.as_view(),name='category-create-list'),
    path('category/<slug:slug>/',CategoryRetrieveUpdateDestroyAPIView.as_view(),name='category-delete-retrieve-update'),
]