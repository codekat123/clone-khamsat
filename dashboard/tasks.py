from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from transaction.models import Order


@shared_task(bind=True, max_retries=3)
def send_deadline_reminders(self):
    try:
        today = timezone.now().date()
        two_days_later = today + timedelta(days=2)

        
        orders = (
            Order.objects
            .select_related('seller__user', 'buyer__user')
            .filter(deadline__range=(today, two_days_later))
        )

        for order in orders:
            seller_name = order.seller.user.first_name or "there"
            buyer_name = order.buyer.user.first_name or "your client"

            subject = f"Hey {seller_name}, your deadline is approaching!"
            message = (
                f"You’ve got just two days left to deliver your project to {buyer_name}.\n\n"
                "Please make sure everything’s on track.\n"
                "Have a productive day!"
            )

            to = order.seller.user.email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to], fail_silently=False)

        return "Deadline reminder emails sent successfully."

    except Exception as e:
        self.retry(exc=e, countdown=10)
        return f"Email sending failed: {e}"


