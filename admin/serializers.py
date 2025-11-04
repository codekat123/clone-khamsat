from rest_framework import serializers
from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
     class Meta:
          model = Service
          fields = '__all__'

# class AboutSellerSerializer(serializers.Serializer):
