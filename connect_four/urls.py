from django.urls import path

from .views import (CreateAIGameView, CreateGameView, DeleteGameView, GameView,
                    IndexView, NewGameView, PlayView)

app_name = 'cf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/', NewGameView.as_view(), name='new_game'),
    path('new_game/<int:pk>/', CreateGameView.as_view(), name='new_game'),
    path('new_game/<slug:slug>/<int:play_as>/', CreateAIGameView.as_view(), name='new_game'),
    path('delete_game/<int:pk>/', DeleteGameView.as_view(), name='delete_game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('game/<int:pk>/<int:col>/', PlayView.as_view(), name='play'),
]
