from django.urls import path
from django.views.generic.base import TemplateView

from .views import LeaderboardView

app_name = 'common'
urlpatterns = [
    path('', TemplateView.as_view(template_name='common/home.html'), name='home'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
