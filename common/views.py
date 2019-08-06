from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import redirect
from django.views import generic


class LeaderboardView(generic.ListView):
    template_name = 'common/leaderboard.html'
    model = get_user_model()
    paginate_by = 10
    ordering = ['-wins', 'losses', 'username']

    def get(self, request, *args, **kwargs):
        try:
            if request.GET['search'] == '':
                return redirect(request.path)
        except KeyError:
            pass
        return super().get(request, args, kwargs)

    def get_queryset(self):
        try:
            if self.request.GET['search'] != '':
                self.queryset = self.model.objects.annotate(
                    similarity=TrigramSimilarity('username', self.request.GET['search'])
                    + TrigramSimilarity('full_name', self.request.GET['search'])
                ).filter(similarity__gt=0.3).order_by('-similarity')
        except KeyError:
            pass
        return super().get_queryset()
