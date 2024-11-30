import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns
from channels.sessions import SessionMiddlewareStack
from core.middleware import CustomAuthMiddleware



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_feed.settings')
# Initialize Django ASGI application early to populate the App Registry
django.setup() 
application = ProtocolTypeRouter({
    "http":  get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        CustomAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})