from django.urls import path
from django.views.generic.base import TemplateView

from .views import LeaderboardView, add_friend, remove_friend

app_name = 'common'
urlpatterns = [
    path('', TemplateView.as_view(template_name='common/home.html'), name='home'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('add_friend/<int:pk>/', add_friend, name='add_friend'),
    path('remove_friend/<int:pk>/', remove_friend, name='remove_friend'),
]
