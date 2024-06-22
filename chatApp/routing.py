from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<uuid:sender_id>/<uuid:receiver_id>/', consumers.MyConsumer.as_asgi())
]