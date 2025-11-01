from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_email_to_seller,notify_the_buyer_accepted_order

@receiver(post_save,sender=Order)
def send_request_order(sender,instance,created,**kwargs):
     if created:
          send_email_to_seller(instance.id)
     
     if instance.status == Order.Status.IN_PROGRESS:
          notify_the_buyer_accepted_order(instance.id)
