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

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        key_cache = f"service_{category_slug}"
        services = cache.get(key_cache)
        if not services:
            service = Service.objects.filter(category__slug=category_slug, is_active=True)
            cache.set(key_cache,service)
        return services


class ServiceCreateAPIView(CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        user = self.request.user.services
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
        user = getattr(self.request.user, 'services', None)
        if user is None:
            return Service.objects.none() 
        return Service.objects.filter(freelancer=self.request.user)

class ServiceDeleteAPIView(DestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    lookup_field = 'slug'

    def get_queryset(self):
        user = getattr(self.request.user, 'services', None)
        if user is None:
            return Service.objects.none() 
        return Service.objects.filter(freelancer=self.request.user)

