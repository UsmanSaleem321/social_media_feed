from django.conf import settings
settings.configure()
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newo.settings")
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from core.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_feed.settings')

application = ProtocolTypeRouter({
     "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
