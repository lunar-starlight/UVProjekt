from django.shortcuts import redirect, get_object_or_404, reverse
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import GameTTT, Player

class IndexView(generic.TemplateView):
    template_name = 'tic_tac_toe/index.html'

def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(Player, pk=p1)
    t2 = get_object_or_404(Player, pk=p2)
    g = GameTTT(p1=t1, p2=t2, play_id=1)
    g.save()
    g.play_id = g.id
    g.save()
    return redirect('ttt:game', g.id, g.id)

class GameView(generic.DetailView):
    model = GameTTT
    template_name = 'tic_tac_toe/game.html'
    context_object_name = 'game'

def play(request, pk: int, _, i: int, j: int):
    g = get_object_or_404(GameTTT, pk=pk)
    g.play(pk, i, j)
    return redirect('ttt:game', pk, pk)

class CreateUserView(generic.CreateView):
    model = Player
    fields = ['name']
