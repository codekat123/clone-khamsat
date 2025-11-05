# from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('auth/',include('users.urls',namespace='users')),
    path('profile/',include('user_profile.urls',namespace='profile')),
    path('services/',include('services.urls',namespace='services')),
    path('transaction/',include('transaction.urls',namespace='transaction')),
    path('chat/',include('chat.urls',namespace='chat')),
    path('rating/',include('rating.urls',namespace='rating')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),
    path('wallet/',include('wallet.urls',namespace='wallet')),
    path('admin/',include('admin.urls',namespace='admin')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)