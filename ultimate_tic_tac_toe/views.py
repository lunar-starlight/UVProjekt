from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from common.views import SearchView

from .models import GameTTT, GameUTTT
from .models import GameUTTT_ChildGame as Child


class IndexView(SearchView):
    template_name = 'ultimate_tic_tac_toe/index.html'
    queryset = GameUTTT.objects.filter(game_over=False)
    context_object_name = 'games'
    model = GameUTTT
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(get_user_model(), pk=p1)
    t2 = get_object_or_404(get_user_model(), pk=p2)
    game = GameTTT(p1=t1, p2=t2)
    game.save()
    g = GameUTTT(p1=t1, p2=t2, game=game)
    g.save()

    for i in range(3):
        for j in range(3):
            child = Child.new_game(g, i, j)
            if child is not None:
                child.play_id = g.id
                child.play_url = 'uttt:play'
                child.save()

    return redirect('uttt:game', g.id)


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


class PlayView(LoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    pattern_name = 'uttt:game'

    def get_redirect_url(self, *args, **kwargs):
        g = get_object_or_404(GameUTTT, pk=kwargs['pk'])
        g.play(kwargs['i'], kwargs['j'])
        del kwargs['i']
        del kwargs['j']
        return super().get_redirect_url(*args, **kwargs)

    def test_func(self):
        g: GameUTTT = get_object_or_404(GameUTTT, pk=self.kwargs['pk'])
        return self.request.user == g.current_player()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class PickView(LoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    pattern_name = 'uttt:game'

    def get_redirect_url(self, *args, **kwargs):
        g = get_object_or_404(GameUTTT, pk=kwargs['pk'])
        g.pick(kwargs['row'], kwargs['col'], kwargs['i'], kwargs['j'])
        return super().get_redirect_url(*args, kwargs['pk'])

    def test_func(self):
        g: GameUTTT = get_object_or_404(GameUTTT, pk=self.kwargs['pk'])
        return self.request.user == g.current_player()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'ultimate_tic_tac_toe/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
