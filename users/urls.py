from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_name = 'users'


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('otp/resend/', ResendOTPAPIView.as_view(), name='resend_otp'),
    path('activate/', VerifyOTPAPIView.as_view(), name='activate'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
]