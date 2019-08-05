from django.urls import path

from .views import GameView, IndexView, new_game, play

app_name = 'cf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/<int:p1>/<int:p2>/', new_game, name='new_game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('game/<int:pk>/<int:col>/', play, name='play'),
]