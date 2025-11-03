from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework.exceptions import ValidationError
from .models import WalletTransaction,Wallet
from .serializers import WalletTransactionSerializer, WalletSerializer
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class WalletTransactionCreateAPIView(CreateAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        wallet = user.wallet
        amount_cents = int(serializer.validated_data.get('amount_cents'))
        transaction_type = serializer.validated_data.get('transaction_type')
        to_user = serializer.validated_data.get('to_user')
        idempotency_key = serializer.validated_data.get('idempotency_key')
        note = serializer.validated_data.get('note')

        if amount_cents <= 0:
            raise ValidationError("Amount must be greater than zero.")

        with transaction.atomic():
            # lock sender wallet
            wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)

            if transaction_type == WalletTransaction.Type.WITHDRAW:
                if wallet.balance_cents < amount_cents:
                    raise ValidationError("Insufficient balance.")
                wallet.balance_cents -= amount_cents
                wallet.save(update_fields=["balance_cents", "updated_at"])

                WalletTransaction.objects.create(
                    wallet=wallet,
                    amount_cents=-amount_cents,
                    transaction_type=WalletTransaction.Type.WITHDRAW,
                    note=note,
                )

            elif transaction_type == WalletTransaction.Type.DEPOSIT:
                wallet.balance_cents += amount_cents
                wallet.save(update_fields=["balance_cents", "updated_at"])

                WalletTransaction.objects.create(
                    wallet=wallet,
                    amount_cents=amount_cents,
                    transaction_type=WalletTransaction.Type.DEPOSIT,
                    note=note,
                )

            elif transaction_type == WalletTransaction.Type.TRANSFER:
                if not to_user:
                    raise ValidationError("You must specify a recipient.")
                if to_user == user:
                    raise ValidationError("You cannot transfer money to yourself.")

                recipient_wallet = to_user.wallet

                from .services import transfer_funds
                transfer_funds(
                    sender_user=user,
                    recipient_user=to_user,
                    amount_cents=amount_cents,
                    idempotency_key=idempotency_key,
                    note=note,
                )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["new_balance_cents"] = request.user.wallet.balance_cents
        return Response(response.data, status=status.HTTP_201_CREATED)


class WalletRetrieveAPIView(RetrieveAPIView):
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.user.wallet
    
    def retrieve(self,request,*args,**kwargs):
        wallet = self.get_object()
        serializer = self.get_serializer(wallet)
        data = serializer.data
        data['transaction_count'] = wallet.transactions.count()
        data['transaction_count'] = wallet.transactions.last().create_at if wallet.transactions.exists() else None
        return Response(data)