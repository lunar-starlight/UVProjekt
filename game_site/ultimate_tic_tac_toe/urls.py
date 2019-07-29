from django.urls import path

from . import views

app_name = 'uttt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('game/<int:pk>/', views.game, name='game'),
    path('play/<int:pk>/<int:i>/<int:j>/', views.play, name='play'),
    path('play/<int:pk>/<int:row>/<int:col>/<int:i>/<int:j>/', views.pick, name='play'),
    path('new_game/<int:p1>/<int:p2>/', views.new_game, name='new_game'),
]
