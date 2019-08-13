from django.urls import path

from .views import CreateGameView, GameView, IndexView, NewGameView, PlayView, CreateAIGameView

app_name = 'ttt'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/', NewGameView.as_view(), name='new_game'),
    path('new_game/<int:pk>/', CreateGameView.as_view(), name='new_game'),
    path('new_game/ai/<slug:slug>/', CreateAIGameView.as_view(), name='new_ai_game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('game/<int:pk>/<int:i>/<int:j>/', PlayView.as_view(), name='play'),
]
