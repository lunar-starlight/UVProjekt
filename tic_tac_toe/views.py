from django.views import generic

from common.views import (BaseCreateAIGameView, BaseCreateGameView,
                          BaseIndexView, BaseNewGameView, BasePlayView)

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

    def get_object(self, queryset=None):
        obj: GameTTT = super().get_object(queryset)
        if obj.current_player().username == 'ai':
            obj.play(-1, -1)
        return obj


class PlayView(BasePlayView):
    pattern_name = 'ttt:game'
    model = GameTTT
    play_args = ['i', 'j']


class NewGameView(BaseNewGameView):
    template_name = 'tic_tac_toe/new_game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ai_list'] = AI_list
        return context


class CreateAIGameView(BaseCreateAIGameView):
    pattern_name = 'ttt:game'
    AI_list = AI_list
