from rest_framework import serializers
from .models import Order, Transaction



class OrderSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
     order = OrderSerializer(read_only=True)
     class Meta:
          model = Transaction
          fields = '__all__'
     
     def get_total_after_commission(self, obj):
        return obj.order.total_price - obj.commission
     

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
