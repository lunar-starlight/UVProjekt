from django.views import generic

from common.views import (BaseCreateGameView, BaseNewGameView, BasePlayView,
                          SearchView)

from .models import GameCF


class IndexView(SearchView):
    template_name = 'connect_four/index.html'
    queryset = GameCF.objects.filter(game_over=False)
    context_object_name = 'game_list'
    model = GameCF
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


class CreateGameView(BaseCreateGameView):
    pattern_name = 'cf:game'
    model = GameCF


class GameView(generic.DetailView):
    model = GameCF
    template_name = 'connect_four/game.html'
    context_object_name = 'game'


class PlayView(BasePlayView):
    pattern_name = 'cf:game'
    model = GameCF
    play_args = ['col']


class NewGameView(BaseNewGameView):
    template_name = 'connect_four/new_game.html'
