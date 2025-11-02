from rest_framework import serializers 
from .models import Rating
from services.serializers  import ServiceSerializer


class RatingSerializer(serializers.ModelSerializer):
     service = ServiceSerializer(read_only=True)

     class Meta:
          model = Rating
          fields = '__all__'
