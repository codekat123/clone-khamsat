from rest_framework import serializers
from .models import Order
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_deadline(self, value):
        if value < timezone.now().date():
            raise ValidationError("Deadline cannot be in the past.")
        return value



     

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = ['status']

     def validate_status(self, value):
          if self.instance.status == Order.Status.COMPLETED:
              raise serializers.ValidationError("Completed orders cannot be changed.") 
          allowed = {
              Order.Status.PENDING: [Order.Status.IN_PROGRESS, Order.Status.CANCELLED],
              Order.Status.IN_PROGRESS: [Order.Status.COMPLETED, Order.Status.CANCELLED],
          }
          if value not in allowed.get(self.instance.status, []):
               raise serializers.ValidationError(f"Cannot change from {self.instance.status} to {value}.")
          return value
