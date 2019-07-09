from django.urls import path

from . import views

app_name = 'ttt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_game/<int:p1>/<int:p2>/', views.new_game, name='new_game'),
    path('game/<int:pk>/', views.game, name='game'),
    path('gameover/<int:pk>/', views.gameover, name='gameover'),
    path('game/<int:pk>/<int:i>/<int:j>/', views.play, name='play'),
    # path('user/', views.create_user_form, name='create_user_form'),
    path('user/<str:name>/', views.create_user, name='create_user'),
]