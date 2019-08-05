from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .models import GameCF


class IndexView(generic.TemplateView):
    template_name = 'connect_four/index.html'


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
