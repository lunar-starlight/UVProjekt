from django.urls import path

from .views import GameView, IndexView, NewGameView, new_game, PlayView

app_name = 'ttt'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/', NewGameView.as_view(), name='new_game'),
    path('new_game/<int:p1>/<int:p2>/', new_game, name='new_game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('game/<int:pk>/<int:i>/<int:j>/', PlayView.as_view(), name='play'),
]
