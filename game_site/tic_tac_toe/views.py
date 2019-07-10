from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import Game, Player

class IndexView(generic.TemplateView):
    template_name = 'tic_tac_toe/index.html'


def new_game(request, p1, p2):
    t1 = get_object_or_404(Player, pk=p1)
    t2 = get_object_or_404(Player, pk=p2)
    g = Game(p1=t1, p2=t2)
    g.save()
    return redirect('ttt:game', g.id)


class GameView(generic.DetailView):
    model = Game
    template_name = 'tic_tac_toe/game.html'


# def game(request, pk):
#     g = get_object_or_404(Game, pk=pk)
#     return render(request, 'tic_tac_toe/game.html', g.context())


def play(request, pk, i, j):
    g = Game.objects.get(id=pk)
    g.play(i, j)
    g.save()
    return redirect('ttt:game', pk)


# def gameover(request, pk):
#     g = Game.objects.get(id=pk)

#     win = 'The game was tied'
#     if g.winner == 1:
#         win = 'Player 1 won'
#     if g.winner == 2:
#         win = 'Player 2 won'
    
#     # Maybe do that elsewhere?
#     # Do I even want this?
#     # g.delete()

#     return render(request, 'tic_tac_toe/gameover.html', {'win_str': win})

class CreateUserView(generic.CreateView):
    model = Player
    fields = ['name']


# def create_user(request, name):
#     p = Player()

#     p.name = name
#     p.save()

#     return redirect('ttt:index')