from django.shortcuts import get_object_or_404
from .models import Category, Service
from .serializers import CategorySerializer,ServiceSerializer
from django.core.cache import cache
from user_profile.permissions import IsSeller,IsBuyer,IsAdminOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from django.core.exceptions import ValidationError

class CategoryCreateListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]





class ServiceListAPIView(ListAPIView):
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'category__name']
    filterset_fields = {'price': ['gte', 'lte']}
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        cache_key = f"services_{category_slug}"
        
        services = cache.get(cache_key)
        if not services:
            services = Service.objects.filter(
                category__slug=category_slug,
                is_active=True
            ).select_related('category')  
            cache.set(cache_key, services, timeout=60 * 5)  
        
        return services



class ServiceSellerListAPIView(ListAPIView):
    serializer = ServiceSerializer
    permission_classes = [IsAuthenticated,IsSeller]

    def get_queryset(self):
        return Service.objects.filter(freelancer__user=self.request.user)


class ServiceCreateAPIView(CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        user = self.request.user.seller_profile
        count = Service.objects.filter(seller=user).count()
        if count > 5:
            raise ValidationError('you cannot create more than five serives ')
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        serializer.save(freelancer=user, category=category)


class ServiceDetailAPIView(RetrieveAPIView):
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        slug = self.kwargs['slug']
        try:
            return Service.objects.get(slug=slug)
        except Service.DoesNotExist:
            raise NotFound('this service does not exist')



class ServiceUpdateAPIView(UpdateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    lookup_field = 'slug'

    def get_queryset(self):
        user = getattr(self.request.user, 'seller_profile', None)
        slug = self.kwargs['slug']
        if user is None:
            return Service.objects.none() 
        return Service.objects.filter(freelancer=user,slug=slug)

class ServiceDeleteAPIView(DestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    lookup_field = 'slug'

    def get_queryset(self):
        user = getattr(self.request.user, 'seller_profile', None)
        slug = self.kwargs['slug']
        if user is None:
            return Service.objects.none() 
        return Service.objects.filter(freelancer=user,slug=slug)

