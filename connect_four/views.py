from django.views import generic

from common.views import (BaseCreateAIGameView, BaseCreateGameView,
                          BaseIndexView, BaseNewGameView, BasePlayView)

from .ai import (BNSAI, MTDFAI, NegamaxPrunningTTTAI, NegamaxTTTAI,
                 NegimaxABTablesAI, PrincipalVariationSearchAI, RandomCFAI)
from .models import GameCF

AI_list = [BNSAI, MTDFAI, NegamaxTTTAI, NegamaxPrunningTTTAI,
           NegimaxABTablesAI, PrincipalVariationSearchAI, RandomCFAI]


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
