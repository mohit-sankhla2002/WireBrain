from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<int:sender_id>/<int:receiver_id>/', consumers.MyConsumer.as_asgi())
]