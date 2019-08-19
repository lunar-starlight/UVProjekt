from django.views import generic

from common.views import (BaseCreateAIGameView, BaseCreateGameView,
                          BaseDeleteGameView, BaseIndexView, BaseNewGameView,
                          BasePlayView)

from .ai import RandomUTTTAI
from .models import GameUTTT

AI_list = [RandomUTTTAI]


class IndexView(BaseIndexView):
    template_name = 'ultimate_tic_tac_toe/index.html'
    model = GameUTTT
    queryset = model.objects.filter(game_over=False)


class CreateGameView(BaseCreateGameView):
    pattern_name = 'uttt:game'
    model = GameUTTT


class GameView(generic.DetailView):
    model = GameUTTT
    template_name = 'ultimate_tic_tac_toe/game.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g: GameUTTT = context['game']
        context['free_pick'] = g.is_free_pick()
        context['my_turn'] = g.current_player() == self.request.user
        return context


class PlayView(BasePlayView):
    pattern_name = 'uttt:game'
    model = GameUTTT
    play_args = ['i', 'j']


class PickView(BasePlayView):
    pattern_name = 'uttt:game'
    model = GameUTTT
    play_args = ['i', 'j', 'row', 'col']


class NewGameView(BaseNewGameView):
    template_name = 'ultimate_tic_tac_toe/new_game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ai_list'] = AI_list
        return context


class CreateAIGameView(BaseCreateAIGameView):
    pattern_name = 'uttt:game'
    AI_list = AI_list


class DeleteGameView(BaseDeleteGameView):
    pattern_name = 'uttt:index'
    model = GameUTTT
