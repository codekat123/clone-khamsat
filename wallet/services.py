from django.db import transaction
from django.core.exceptions import ValidationError

def transfer_funds(sender_user, recipient_user, amount_cents, idempotency_key=None, note=None):
    with transaction.atomic():
        sender_wallet = sender_user.wallet
        recipient_wallet = recipient_user.wallet

        # Lock rows to prevent race conditions
        sender_wallet = sender_wallet.__class__.objects.select_for_update().get(pk=sender_wallet.pk)
        recipient_wallet = recipient_wallet.__class__.objects.select_for_update().get(pk=recipient_wallet.pk)

        if sender_wallet.balance < amount_cents:
            raise ValidationError('Insufficient balance.')

        sender_wallet.balance -= amount_cents
        recipient_wallet.balance += amount_cents

        sender_wallet.save()
        recipient_wallet.save()

        # Optionally record transactions for both users
        sender_wallet.transactions.create(
            transaction_type='TRANSFER',
            amount=amount_cents,
            note=note,
            to_user=recipient_user,
        )
        recipient_wallet.transactions.create(
            transaction_type='DEPOSIT',
            amount=amount_cents,
            note=f'Received from {sender_user}',
        )
