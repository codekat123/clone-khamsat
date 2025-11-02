from django.shortcuts import get_object_or_404
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from user_profile.permissions import IsBuyer
from services.models import Service
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from transaction.models import Order

class RatingListCreateAPIView(ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsBuyer]

    def get_queryset(self):
        slug = self.kwargs['slug']
        service = get_object_or_404(Service, slug=slug)
        return Rating.objects.filter(service=service)

    def perform_create(self, serializer):
        buyer = self.request.user.buyer_profile
        slug = self.kwargs['slug']
        service = get_object_or_404(Service, slug=slug)

        has_completed_order = Order.objects.filter(
            service=service,
            buyer=buyer,
            status=Order.Status.COMPLETED
        ).exists()

        if not has_completed_order:
            raise ValidationError("You can only rate after completing your order.")

        old_rating = Rating.objects.filter(user=buyer, service=service).first()

        if old_rating:
            old_rating.comment = serializer.validated_data['comment']
            old_rating.stars = serializer.validated_data['stars']
            old_rating.save()
        else:
            serializer.save(user=buyer, service=service)


class RatingDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsBuyer]

    def get_queryset(self):
        buyer = self.request.user.buyer_profile
        return Rating.objects.filter(user=buyer)


@api_view(['GET'])
def get_average_rating_of_service(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)
    ratings = Rating.objects.filter(service=service)
    
    if not ratings.exists():
        return Response(
            {'average': 0, 'message': 'No ratings yet for this service.'},
            status=status.HTTP_200_OK
        )
    
    total = sum(rating.stars for rating in ratings)
    average = total / ratings.count()

    return Response(
        {'average': round(average, 2)},
        status=status.HTTP_200_OK
    )
