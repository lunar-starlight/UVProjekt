from django.urls import path

from .views import IndexView, NewGameView, game, new_game, pick, play

app_name = 'uttt'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_game/', NewGameView.as_view(), name='new_game'),
    path('new_game/<int:p1>/<int:p2>/', new_game, name='new_game'),
    path('game/<int:pk>/', game, name='game'),
    path('play/<int:pk>/<int:i>/<int:j>/', play, name='play'),
    path('play/<int:pk>/<int:row>/<int:col>/<int:i>/<int:j>/', pick, name='play'),
]
