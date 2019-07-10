from django.urls import path

from . import views

app_name = 'ttt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_game/<int:p1>/<int:p2>/', views.new_game, name='new_game'),
    path('game/<int:pk>/<int:_>/', views.GameView.as_view(), name='game'),
    path('game/<int:pk>/<int:_>/<int:i>/<int:j>/', views.play, name='play'),
    path('user/', views.CreateUserView.as_view(), name='create_user'),
]