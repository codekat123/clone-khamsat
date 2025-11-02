from django.db import models
from django.contrib.auth import get_user_model
from transaction.models import Order
User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance_cents = models.BigIntegerField(default=0)  
    updated_at = models.DateTimeField(auto_now=True)

class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT'
        WITHDRAW = 'WITHDRAW'
        TRANSFER = 'TRANSFER'
        ESCROW_HOLD = 'ESCROW_HOLD'
        ESCROW_RELEASE = 'ESCROW_RELEASE'
        REFUND = 'REFUND'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount_cents = models.BigIntegerField()
    transaction_type = models.CharField(max_length=20, choices=Type.choices)
    related_order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    counterparty = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.SET_NULL, related_name='incoming_transfers')
    idempotency_key = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['idempotency_key']),
            models.Index(fields=['created_at']),
        ]

