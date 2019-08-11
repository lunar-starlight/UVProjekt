from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from common.views import BasePlayView, SearchView

from .models import GameCF


class IndexView(SearchView):
    template_name = 'connect_four/index.html'
    queryset = GameCF.objects.filter(game_over=False)
    context_object_name = 'game_list'
    model = GameCF
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


class CreateGameView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'cf:game'

    def get_redirect_url(self, *args, **kwargs):
        p2 = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        g = GameCF(p1=self.request.user, p2=p2)
        g.save()
        return super().get_redirect_url(*args, g.pk)


class GameView(generic.DetailView):
    model = GameCF
    template_name = 'connect_four/game.html'
    context_object_name = 'game'


class PlayView(BasePlayView):
    pattern_name = 'cf:game'
    model = GameCF
    play_args = ['col']


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'connect_four/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
