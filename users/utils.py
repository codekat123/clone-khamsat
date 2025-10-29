import random
from django.core.cache import cache

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email, otp):
    cache.set(f"otp_{email}", otp, timeout=300)  

def verify_otp(email, otp):
    saved_otp = cache.get(f"otp_{email}")
    if saved_otp and saved_otp == otp:
        cache.delete(f"otp_{email}")
        return True
    return False
