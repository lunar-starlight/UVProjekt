from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import GameUTTT, GameTTT, Player

class IndexView(generic.TemplateView):
    template_name = 'ultimate_tic_tac_toe/index.html'

def new_game(request, p1, p2):
    t1 = get_object_or_404(Player, pk=p1)
    t2 = get_object_or_404(Player, pk=p2)
    g0 = GameTTT(p1=t1, p2=t2, keep_score=False); g0.save()
    g1 = GameTTT(p1=t1, p2=t2, keep_score=False); g1.save()
    g2 = GameTTT(p1=t1, p2=t2, keep_score=False); g2.save()
    g3 = GameTTT(p1=t1, p2=t2, keep_score=False); g3.save()
    g4 = GameTTT(p1=t1, p2=t2, keep_score=False); g4.save()
    g5 = GameTTT(p1=t1, p2=t2, keep_score=False); g5.save()
    g6 = GameTTT(p1=t1, p2=t2, keep_score=False); g6.save()
    g7 = GameTTT(p1=t1, p2=t2, keep_score=False); g7.save()
    g8 = GameTTT(p1=t1, p2=t2, keep_score=False); g8.save()
    game = GameTTT(p1=t1, p2=t2); game.save()
    g = GameUTTT(p1=t1, p2=t2, g0=g0, g1=g1, g2=g2, g3=g3, g4=g4, g5=g5, g6=g6, g7=g7, g8=g8, game=game)
    g.games = [g.g0.id, g.g1.id, g.g2.id, g.g3.id, g.g4.id, g.g5.id, g.g6.id, g.g7.id, g.g8.id]
    g.save()
    return redirect('uttt:game', g.id)

def game(request, pk):
    g = get_object_or_404(GameUTTT, pk=pk)

    template = loader.get_template('tic_tac_toe/game.html')

    context = {'game': g}
    context['g0'] = template.render({'game': g.g0}, request)
    context['g1'] = template.render({'game': g.g1}, request)
    context['g2'] = template.render({'game': g.g2}, request)
    context['g3'] = template.render({'game': g.g3}, request)
    context['g4'] = template.render({'game': g.g4}, request)
    context['g5'] = template.render({'game': g.g5}, request)
    context['g6'] = template.render({'game': g.g6}, request)
    context['g7'] = template.render({'game': g.g7}, request)
    context['g8'] = template.render({'game': g.g8}, request)

    return render(request, 'ultimate_tic_tac_toe/game.html', context=context)