import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_feed.settings')

import django
from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from core.routing import websocket_urlpatterns

# Set the environment variable for Django settings module


# Initialize Django
django.setup()

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

