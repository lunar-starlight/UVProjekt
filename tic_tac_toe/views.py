from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from common.views import SearchView

from .models import GameTTT


class IndexView(SearchView):
    template_name = 'tic_tac_toe/index.html'
    queryset = GameTTT.objects.filter(game_over=False, keep_score=True).exclude(play_id=0)
    context_object_name = 'games'
    model = GameTTT
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(get_user_model(), pk=p1)
    t2 = get_object_or_404(get_user_model(), pk=p2)
    g = GameTTT(p1=t1, p2=t2, play_id=1)
    g.save()
    g.play_id = g.id
    g.save()
    return redirect('ttt:game', g.id)


class GameView(generic.DetailView):
    model = GameTTT
    template_name = 'tic_tac_toe/game.html'
    context_object_name = 'game'


class PlayView(LoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    pattern_name = 'ttt:game'

    def get_redirect_url(self, *args, **kwargs):
        g = get_object_or_404(GameTTT, pk=kwargs['pk'])
        g.play(kwargs['i'], kwargs['j'])
        return super().get_redirect_url(*args, kwargs['pk'])

    def test_func(self):
        g: GameTTT = get_object_or_404(GameTTT, pk=self.kwargs['pk'])
        return self.request.user == g.current_player()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'tic_tac_toe/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
