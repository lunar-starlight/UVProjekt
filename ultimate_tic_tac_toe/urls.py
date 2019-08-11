from django.urls import path

from .views import (CreateGameView, GameView, IndexView, NewGameView, PickView,
                    PlayView)

app_name = 'uttt'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/', NewGameView.as_view(), name='new_game'),
    path('new_game/<int:pk>/', CreateGameView.as_view(), name='new_game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('play/<int:pk>/<int:i>/<int:j>/', PlayView.as_view(), name='play'),
    path('play/<int:pk>/<int:row>/<int:col>/<int:i>/<int:j>/', PickView.as_view(), name='play'),
]
