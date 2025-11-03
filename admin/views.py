from rest_framework.generics import ListAPIView
from django.core.cache import cache
from services.models import Service
from services.serializers import ServiceSerializer
from user_profile.permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

class BaseServiceListAPIView(ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self, *, is_active=True, cache_key=None):
        services = cache.get(cache_key)
        if not services:
            services = list(
                Service.objects
                .select_related('seller', 'seller__user')
                .filter(is_active=is_active)
            )
            cache.set(cache_key, services, timeout=86400)
        return services


class ActiveServiceAPIView(BaseServiceListAPIView):
    def get_queryset(self):
        return super().get_queryset(is_active=True, cache_key='active_services')


class InactiveServiceAPIView(BaseServiceListAPIView):
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return super().get_queryset(is_active=False, cache_key='inactive_services')


class ActivateServiceAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        slug = request.data.get('slug')

        if not slug:
            raise ValidationError("You must provide a service slug.")

        service = get_object_or_404(Service, slug=slug)

        if service.is_active:
            return Response(
                {"message": "Service is already active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service.is_active = True
        service.save()

        
        cache.delete('inactive_services')
        cache.delete('active_services')

        return Response(
            {"message": f"Service '{service.title}' has been activated successfully."},
            status=status.HTTP_200_OK
        )
    
class 