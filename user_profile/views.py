from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import SellerProfile, BuyerProfile
from .serializers import SellerProfileSerializer, BuyerProfileSerializer
from .permissions import IsSeller , IsBuyer
User = get_user_model()


class SellerProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsSeller]

    def get_object(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user
        return get_object_or_404(SellerProfile, user=user)


class BuyerProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsBuyer]

    def get_object(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user
        return get_object_or_404(BuyerProfile, user=user)

