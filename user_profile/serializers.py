from rest_framework import serializers 
from .models import SellerProfile , BuyerProfile



class SellerProfileSerializer(serializers.ModelSerializer):
     class Meta:
          model = SellerProfile
          fields = '__all__'
          read_only_fields = ['balance', 'created_at', 'updated_at',]

     def validate_bio(self, value):
          if len(value) < 10:
              raise serializers.ValidationError("Bio must be at least 10 characters.")
          return value

class BuyerProfileSerializer(serializers.ModelSerializer):
     class Meta:
          model = BuyerProfile
          fields = '__all__'
          read_only_fields = ['balance', 'created_at', 'updated_at',]

     def validate_bio(self, value):
          if len(value) < 10:
              raise serializers.ValidationError("Bio must be at least 10 characters.")
          return value
     