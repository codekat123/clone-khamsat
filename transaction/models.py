from django.db import models
from user_profile.models import BuyerProfile , SellerProfile
from services.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        REJECTED = 'rejected', 'Rejected'

    buyer = models.ForeignKey(
        BuyerProfile,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True, blank=True
    )
    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    price = models.DecimalField(max_digits=5,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"




class Transaction(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='transaction')
    commission = models.DecimalField(max_digits=2,decimal_places=1)
    create_at = models.DateTimeField(auto_now_add=True)

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='status_history')
    chanaged = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='status_history',null=True)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
