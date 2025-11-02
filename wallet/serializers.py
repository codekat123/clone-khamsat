from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Wallet, WalletTransaction

User = get_user_model()

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']
        read_only_fields = ['user', 'balance']


class WalletTransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = WalletTransaction
        fields = '__all__'

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Transaction amount must be greater than zero.")
        return value

