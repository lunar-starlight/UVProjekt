from django.shortcuts import redirect, get_object_or_404, reverse
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import Game, Player

class IndexView(generic.TemplateView):
    template_name = 'tic_tac_toe/index.html'

def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(Player, pk=p1)
    t2 = get_object_or_404(Player, pk=p2)
    g = Game(p1=t1, p2=t2, play_id=1)
    g.save()
    g.play_id = g.id
    g.save()
    return redirect('ttt:game', g.id)

class GameView(generic.DetailView):
    model = Game
    template_name = 'tic_tac_toe/game.html'

def play(request, pk: int, i: int, j: int):
    g = get_object_or_404(Game, pk=pk)
    g.play(i, j)
    g.save()
    return redirect('ttt:game', pk)

class CreateUserView(generic.CreateView):
    model = Player
    fields = ['name']
