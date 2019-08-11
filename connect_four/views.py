from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from common.views import SearchView

from .models import GameCF


class IndexView(SearchView):
    template_name = 'connect_four/index.html'
    queryset = GameCF.objects.filter(game_over=False)
    context_object_name = 'games'
    model = GameCF
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}


def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(get_user_model(), pk=p1)
    t2 = get_object_or_404(get_user_model(), pk=p2)
    g = GameCF(p1=t1, p2=t2)
    g.save()
    return redirect('cf:game', g.pk)


class GameView(generic.DetailView):
    model = GameCF
    template_name = 'connect_four/game.html'
    context_object_name = 'game'


def play(request, pk: int, col: int):
    g = get_object_or_404(GameCF, pk=pk)
    print(f"play game {pk} at {col}")
    g.play(col)
    return redirect('cf:game', pk)


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'connect_four/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
