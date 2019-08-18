from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/ttt/game/<int:pk>/', consumers.GameConsumer),
]
