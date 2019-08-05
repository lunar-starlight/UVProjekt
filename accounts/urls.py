from django.urls import path

from . import views

appname = 'accounts'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]