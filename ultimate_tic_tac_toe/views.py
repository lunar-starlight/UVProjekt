from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from common.views import BasePlayView, SearchView

from .models import GameUTTT
from .models import GameUTTT_ChildGame as Child


class IndexView(SearchView):
    template_name = 'ultimate_tic_tac_toe/index.html'
    queryset = GameUTTT.objects.filter(game_over=False)
    context_object_name = 'game_list'
    model = GameUTTT
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


class CreateGameView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'uttt:game'

    def get_redirect_url(self, *args, **kwargs):
        p2 = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        g = GameUTTT(p1=self.request.user, p2=p2)
        return super().get_redirect_url(*args, g.pk)


class GameView(generic.DetailView):
    model = GameUTTT
    template_name = 'ultimate_tic_tac_toe/game.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g: GameUTTT = context['game']
        context['free_pick'] = Child.get_game(g, g.prev_i, g.prev_j).winner != 0
        context['my_turn'] = g.current_player() == self.request.user
        return context


class PlayView(BasePlayView):
    pattern_name = 'uttt:game'
    model = GameUTTT
    play_args = ['i', 'j']


class PickView(BasePlayView):
    pattern_name = 'uttt:game'
    model = GameUTTT
    play_args = ['row', 'col', 'i', 'j']

    def get_redirect_url(self, *args, **kwargs):
        g = get_object_or_404(self.model, pk=kwargs['pk'])
        g.pick(*(kwargs[s] for s in self.play_args))
        return super(BasePlayView, self).get_redirect_url(*args, kwargs['pk'])


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'ultimate_tic_tac_toe/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
