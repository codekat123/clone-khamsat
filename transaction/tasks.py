from celery import shared_task
from django.conf import settings
from .models import Order
from django.shortcuts import get_object_or_404
import requests
from django.urls import reverse
from django.contrib.sites.models import Site
from django.urls import reverse


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

def send_via_brevo(subject, html_content, to_email, attachments=None):
    """Helper to send an email through Brevo’s API."""
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    data = {
        "sender": {"name": "Shop", "email": settings.DEFAULT_FROM_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }

    if attachments:
        data["attachment"] = attachments

    response = requests.post(BREVO_API_URL, headers=headers, json=data, timeout=10)
    if response.status_code not in (200, 201, 202):
        raise Exception(f"Brevo API error: {response.status_code} - {response.text}")

    return response.json()


@shared_task(bind=True, max_retries=3)
def send_email_to_seller(self, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        subject = f"You’ve received a new order from {order.buyer.user.first_name or 'a new buyer'}"

        current_site = Site.objects.get_current()
        order_url = f"https://{current_site.domain}{reverse('transaction:order-retrieve', args=[order.id])}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>...</head>
        <body>
            <div class="container">
                <h2>🎉 New Order Received!</h2>
                <p>Hey <strong>{order.seller.user.first_name or "Seller"}</strong>,</p>
                <p>You just received a new order from 
                    <strong>{order.buyer.user.first_name or "a new buyer"}</strong>
                    for your service 
                    <strong>{order.service.title}</strong>.
                </p>
                <p>Click below to check the order details:</p>
                <a href="{order_url}" class="btn">View Order</a>
            </div>
        </body>
        </html>
        """

        to = order.seller.user.email
        send_via_brevo(subject, html_content, to)

        return f"Email sent successfully to {to}"

    except Exception as e:
        self.retry(exc=e, countdown=10)
        return f"Email sending failed: {e}"

     
@shared_task(bind=True,max_tries=3)
def notify_the_buyer_accepted_order(self,order_id):
    try:
        order = get_object_or_404(Order,id=order_id)
        current_site = Site.objects.get_current()
        order_url = f"https://{current_site.domain}{reverse('transaction:order-retrieve', args=[order.id])}"
        subject = f"your order has been accepted"
        to = order.buyer.user.email
        html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <title>Order Accepted</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9fafc;
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .btn {{
                display: inline-block;
                margin-top: 15px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            .btn:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>✅ Your Order Has Been Accepted!</h2>
            <p>Hi <strong>{order.buyer.user.first_name or "Buyer"}</strong>,</p>
            <p>Good news! The seller <strong>{order.seller.user.first_name or "the seller"}</strong> 
            has accepted your order for the service <strong>{order.service.title}</strong>.</p>
            <p>You can now track your order progress and communicate with the seller directly.</p>
            <a href="{order_url}" class="btn">View Order</a>
            <p style="margin-top: 20px;">Thank you for using our platform 💚</p>
        </div>
    </body>
    </html>
    """
        send_via_brevo(subject,html_content,to)
        return f"email sent successfully to {to}"
    except Exception as e:
        self.retry(exc=e, countdown=10)
        return f"Email sending failed: {e}"

