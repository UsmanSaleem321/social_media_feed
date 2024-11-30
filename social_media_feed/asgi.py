import os
import django
django.setup() 
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_feed.settings')
# Initialize Django ASGI application early to populate the App Registry

application = ProtocolTypeRouter({
    "http":  get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
})