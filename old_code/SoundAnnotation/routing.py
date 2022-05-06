from django.conf.urls import url

from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from SoundAnnotation.consumers import SoundAnnotation_WebSocketConsumer

# Consumer Imports
from WebApp.consumers import WebAppConsumer


application = ProtocolTypeRouter({

    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/$", SoundAnnotation_WebSocketConsumer.as_asgi()),
        ])
    ),
    "channel": ChannelNameRouter({
        "WebApp": WebAppConsumer,
    })
})
