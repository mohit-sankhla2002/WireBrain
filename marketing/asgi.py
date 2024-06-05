import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chatApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbchat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        chatApp.routing.websocket_urlpatterns
    )
})
