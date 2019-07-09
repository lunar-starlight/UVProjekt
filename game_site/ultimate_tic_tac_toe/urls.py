from django.urls import path

from . import views

app_name='uttt'
urlpatterns = [
    path('', views.index, name='index'),
]