from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

application = get_asgi_application()

import src.routing
application = ProtocolTypeRouter({
     'http':application,
     'websocket':AuthMiddlewareStack(
          URLRouter(src.routing.websocket_urlpatterns)
     ),
})