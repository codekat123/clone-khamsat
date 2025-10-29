from celery import shared_task
from django.core.mail import send_mail
from .utils import generate_otp, store_otp

@shared_task
def send_otp_email(email):
    otp = generate_otp()
    store_otp(email, otp)
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}",
        from_email="your_email@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )
