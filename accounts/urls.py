from django.urls import path

from .views import EditView, SignUpView

appname = 'accounts'
urlpatterns = [
    path('edit/', EditView.as_view(), name='edit'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
