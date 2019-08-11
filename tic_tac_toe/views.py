from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from common.views import SearchView, BasePlayView

from .models import GameTTT


class IndexView(SearchView):
    template_name = 'tic_tac_toe/index.html'
    queryset = GameTTT.objects.filter(game_over=False, keep_score=True).exclude(play_id=0)
    context_object_name = 'game_list'
    model = GameTTT
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


class CreateGameView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'ttt:game'

    def get_redirect_url(self, *args, **kwargs):
        p2 = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        g = GameTTT.new_game(p1=self.request.user, p2=p2)
        return super().get_redirect_url(*args, g.pk)


class GameView(generic.DetailView):
    model = GameTTT
    template_name = 'tic_tac_toe/game.html'
    context_object_name = 'game'


class PlayView(BasePlayView):
    pattern_name = 'ttt:game'
    model = GameTTT
    play_args = ['i', 'j']


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'tic_tac_toe/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
