from django.views import generic

from common.views import (BaseCreateAIGameView, BaseCreateGameView,
                          BaseDeleteGameView, BaseIndexView, BaseNewGameView,
                          BasePlayView)

from .ai import (BNSAI, MTDFAI, NegamaxABTablesAI, NegamaxPruningTTTAI,
                 NegamaxTTTAI, PrincipalVariationSearchAI, RandomCFAI)
from .models import GameCF

AI_list = [BNSAI, MTDFAI, NegamaxTTTAI, NegamaxPruningTTTAI,
           NegamaxABTablesAI, PrincipalVariationSearchAI, RandomCFAI]


class IndexView(BaseIndexView):
    template_name = 'connect_four/index.html'
    model = GameCF
    queryset = model.objects.filter(game_over=False)


class CreateGameView(BaseCreateGameView):
    pattern_name = 'cf:game'
    model = GameCF


class GameView(generic.DetailView):
    model = GameCF
    template_name = 'connect_four/game.html'
    context_object_name = 'game'

    def get_object(self, queryset=None):
        obj: GameCF = super().get_object(queryset)
        if obj.current_player().username == 'ai':
            obj.play(-1)
        return obj


class PlayView(BasePlayView):
    pattern_name = 'cf:game'
    model = GameCF
    play_args = ['col']


class NewGameView(BaseNewGameView):
    template_name = 'connect_four/new_game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ai_list'] = AI_list
        return context


class CreateAIGameView(BaseCreateAIGameView):
    pattern_name = 'cf:game'
    AI_list = AI_list


class DeleteGameView(BaseDeleteGameView):
    pattern_name = 'cf:index'
    model = GameCF
