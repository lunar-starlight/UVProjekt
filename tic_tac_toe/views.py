from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import generic

from .models import GameTTT


class IndexView(generic.ListView):
    template_name = 'tic_tac_toe/index.html'
    queryset = GameTTT.objects.filter(game_over=False, keep_score=True)
    context_object_name = 'games'
    paginate_by = 10
    ordering = ['pk']


def new_game(request, p1: int, p2: int):
    t1 = get_object_or_404(get_user_model(), pk=p1)
    t2 = get_object_or_404(get_user_model(), pk=p2)
    g = GameTTT(p1=t1, p2=t2, play_id=1)
    g.save()
    g.play_id = g.id
    g.save()
    return redirect('ttt:game', g.id)


class GameView(generic.DetailView):
    model = GameTTT
    template_name = 'tic_tac_toe/game.html'
    context_object_name = 'game'


@login_required
def play(request, pk: int, i: int, j: int):
    g = get_object_or_404(GameTTT, pk=pk)
    if g.current_player() == request.user:
        print(f"play game {pk} at ({i}, {j})")
        g.play(i, j)
        return redirect('ttt:game', pk)
    else:
        base_url = reverse('login')
        query_string = 'next='+reverse('ttt:play', args=(pk, i, j))
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
