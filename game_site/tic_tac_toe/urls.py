from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_game/<str:p1>/<str:p2>/', views.new_game, name='new_game'),
    path('game/<int:game_id>/', views.game, name='game'),
    path('gameover/<int:game_id>/', views.gameover, name='gameover'),
    path('game/<int:game_id>/<int:i>/<int:j>/', views.play, name='play'),
    # path('user/', views.create_user_form, name='create_user_form'),
    path('user/<str:name>/', views.create_user, name='create_user'),
]