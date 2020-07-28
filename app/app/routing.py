from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from message.consumers import ChatConsumer

websocket_urlpatterns = [
    path('<str:room_id>', ChatConsumer),
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
