from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import GameTTT, GameUTTT
from .models import GameUTTT_ChildGame as Child


class IndexView(generic.TemplateView):
    template_name = 'ultimate_tic_tac_toe/index.html'


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


def game(request, pk: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)

    p = g.game.get_position(g.prev_i, g.prev_j)

    context = dict()
    context['game'] = g
    context['free_pick'] = g.game.field[p] != '0'

    return render(request, 'ultimate_tic_tac_toe/game.html', context=context)


def play(request, pk: int, i: int, j: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)
    g.play(i, j)
    return redirect('uttt:game', pk)


def pick(request, pk: int, row: int, col: int, i: int, j: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)
    g.pick(row, col, i, j)
    return redirect('uttt:game', pk)
