from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import GameUTTT, GameTTT, Player

class IndexView(generic.TemplateView):
    template_name = 'ultimate_tic_tac_toe/index.html'

def new_game(request, p1: int, p2: int):
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
    g.save()
    g0.play_id = g.id; g0.play_url = 'uttt:play'; g0.save()
    g1.play_id = g.id; g1.play_url = 'uttt:play'; g1.save()
    g2.play_id = g.id; g2.play_url = 'uttt:play'; g2.save()
    g3.play_id = g.id; g3.play_url = 'uttt:play'; g3.save()
    g4.play_id = g.id; g4.play_url = 'uttt:play'; g4.save()
    g5.play_id = g.id; g5.play_url = 'uttt:play'; g5.save()
    g6.play_id = g.id; g6.play_url = 'uttt:play'; g6.save()
    g7.play_id = g.id; g7.play_url = 'uttt:play'; g7.save()
    g8.play_id = g.id; g8.play_url = 'uttt:play'; g8.save()
    return redirect('uttt:game', g.id)

def game(request, pk: int):
    g:GameUTTT = get_object_or_404(GameUTTT, pk=pk)

    template = loader.get_template('tic_tac_toe/game.html')

    context = {'game': g}
    context['g0'] = template.render({'game': g.g0, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g0'}, request)
    context['g1'] = template.render({'game': g.g1, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g1'}, request)
    context['g2'] = template.render({'game': g.g2, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g2'}, request)
    context['g3'] = template.render({'game': g.g3, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g3'}, request)
    context['g4'] = template.render({'game': g.g4, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g4'}, request)
    context['g5'] = template.render({'game': g.g5, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g5'}, request)
    context['g6'] = template.render({'game': g.g6, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g6'}, request)
    context['g7'] = template.render({'game': g.g7, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g7'}, request)
    context['g8'] = template.render({'game': g.g8, 'disabled': 'g' + str(3*g.prev_i + g.prev_j) != 'g8'}, request)

    return render(request, 'ultimate_tic_tac_toe/game.html', context=context)

def play(request, pk: int, i: int, j: int):
    g = get_object_or_404(GameUTTT, pk=pk)
    g.play(i, j)
    return redirect('uttt:game', pk)