
# from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path,re_path

from app1.consumers import MySyncConsumer

websocket_urlpatterns = [

    re_path(r'ws/sc/(?P<user_id>\d+)/$',MySyncConsumer.as_asgi()),
]