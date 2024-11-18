import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_feed.settings')
# Initialize Django ASGI application early to populate the App Registry
django_asgi_app = get_asgi_application()

# Define the ASGI application                                                                                                                                                                               
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol handled by Django ASGI application
    "websocket":AuthMiddlewareStack(  # WebSocket protocol with authentication middleware
        URLRouter(
            websocket_urlpatterns  # Routing for WebSocket URLs
        )
    ),
})
