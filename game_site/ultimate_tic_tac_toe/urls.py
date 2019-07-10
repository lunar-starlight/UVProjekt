from django.urls import path

from . import views

app_name='uttt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('game/<int:pk>/', views.game, name='game'),
    path('play/<int:pk>/<int:fk>/<int:i>/<int:j>/', views.play, name='play'),
    path('new_game/<int:p1>/<int:p2>/', views.new_game, name='new_game'),
]