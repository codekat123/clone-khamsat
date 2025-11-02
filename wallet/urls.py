from django.urls import path
from .views import WalletTransactionCreateAPIView

app_name = 'wallet'


urlpatterns = [
     path('transaction/',WalletTransactionCreateAPIView.as_view(),name='transaction')
]