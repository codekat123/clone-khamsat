from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import SellerProfile , BuyerProfile


@receiver(post_save,sender=User)
def create_profile_user(sender,instance,created,**kwargs):
     if created:
          if instance.is_buyer:
               BuyerProfile.objects.create(user=instance)
          if instance.is_seller:
               SellerProfile.objects.create(user=instance)
          
