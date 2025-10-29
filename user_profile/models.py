from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    bio = models.TextField(max_length=500)
    image = models.ImageField(upload_to='avatars/', default='avatars/seller.jpeg')
    title = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)
    balance = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Seller Profile"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    bio = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='avatars/', default='avatars/buyer.jpeg')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    orders_count = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Buyer Profile"
