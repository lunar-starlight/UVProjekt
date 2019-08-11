from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse

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


@login_required
def game(request, pk: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)

    context = dict()
    context['game'] = g
    context['free_pick'] = Child.get_game(g, g.prev_i, g.prev_j).winner != 0
    context['my_turn'] = g.current_player() == request.user

    return render(request, 'ultimate_tic_tac_toe/game.html', context=context)


@login_required
def play(request, pk: int, i: int, j: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)
    if g.current_player() == request.user:
        g.play(i, j)
        return redirect('uttt:game', pk)
    else:
        base_url = reverse('login')
        query_string = 'next='+reverse('uttt:play', args=(pk, i, j))
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


@login_required
def pick(request, pk: int, row: int, col: int, i: int, j: int):
    g: GameUTTT = get_object_or_404(GameUTTT, pk=pk)
    if g.current_player() == request.user:
        g.pick(row, col, i, j)
        return redirect('uttt:game', pk)
    else:
        base_url = reverse('login')
        query_string = 'next='+reverse('uttt:pick', args=(pk, row, col, i, j))
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


class NewGameView(LoginRequiredMixin, SearchView):
    template_name = 'ultimate_tic_tac_toe/new_game.html'
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
