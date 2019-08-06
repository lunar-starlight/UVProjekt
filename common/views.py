from django.contrib.auth import get_user_model
from django.views import generic


class LeaderboardView(generic.ListView):
    template_name = 'common/leaderboard.html'
    model = get_user_model()
    paginate_by = 10
    ordering = ['-wins', 'losses', 'username']
