from django.views import generic

from common.views import (BaseCreateGameView, BaseIndexView, BaseNewGameView,
                          BasePlayView)

from .ai import MinimaxTTTAI, NegamaxTTTAI, RandomTTTAI
from .models import GameTTT

AI_list = [MinimaxTTTAI, NegamaxTTTAI, RandomTTTAI]


class IndexView(BaseIndexView):
    template_name = 'tic_tac_toe/index.html'
    model = GameTTT
    queryset = model.objects.filter(game_over=False, keep_score=True).exclude(play_id=0)


class CreateGameView(BaseCreateGameView):
    pattern_name = 'ttt:game'
    model = GameTTT


class GameView(generic.DetailView):
    model = GameTTT
    template_name = 'tic_tac_toe/game.html'
    context_object_name = 'game'


class PlayView(BasePlayView):
    pattern_name = 'ttt:game'
    model = GameTTT
    play_args = ['i', 'j']


class NewGameView(BaseNewGameView):
    template_name = 'tic_tac_toe/new_game.html'


class CreateAIGameView(BaseCreateGameView):
    pattern_name = 'ttt:game'
    model = None

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = 1
        for model in AI_list:
            if model.slug == kwargs['slug']:
                self.model = model
        return super().get_redirect_url(*args, **kwargs)
