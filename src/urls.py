from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('users.urls',namespace='users')),
    path('profile/',include('user_profile.urls',namespace='profile')),
    path('services/',include('services.urls',namespace='services')),
    path('transaction/',include('transaction.urls',namespace='transaction')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)