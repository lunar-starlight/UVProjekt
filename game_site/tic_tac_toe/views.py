from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import Game, Player

class IndexView(generic.TemplateView):
    template_name = 'tic_tac_toe/index.html'

def new_game(request, p1, p2):
    g = Game()
    g.p1 = Player.objects.get(name=p1)
    g.p2 = Player.objects.get(name=p2)
    g.save()
    return redirect('ttt:game', g.id)

# class GameView(generic.DetailView):
#     model = Game
#     template_name = 'tic_tac_toe/game.html'

def game(request, game_id):
    g = Game.objects.get(id=game_id)

    if g.winner != 0 or g.field.count('0') == 0:
        return redirect('ttt:gameover', game_id)

    conv = {'0': '', '1': 'X', '2': 'O'}

    field = [[conv[g.field[3*i + j]] for j in range(3)] for i in range(3)]
    template = loader.get_template('tic_tac_toe/game.html')
    context = {
        'game_id': game_id,
        'field': field,
        'field0': conv[g.field[0]],
        'field1': conv[g.field[1]],
        'field2': conv[g.field[2]],
        'field3': conv[g.field[3]],
        'field4': conv[g.field[4]],
        'field5': conv[g.field[5]],
        'field6': conv[g.field[6]],
        'field7': conv[g.field[7]],
        'field8': conv[g.field[8]],
    }
    print(template.render(context, request))
    return HttpResponse(template.render(context, request))
    # return HttpResponse(g.html())
    # return render(request, 'tic_tac_toe/game.html', {
    #     'game_id': game_id,
    #     'field': field,
    #     'field0': conv[g.field[0]],
    #     'field1': conv[g.field[1]],
    #     'field2': conv[g.field[2]],
    #     'field3': conv[g.field[3]],
    #     'field4': conv[g.field[4]],
    #     'field5': conv[g.field[5]],
    #     'field6': conv[g.field[6]],
    #     'field7': conv[g.field[7]],
    #     'field8': conv[g.field[8]],
    # })

def play(request, game_id, i, j):
    g = Game.objects.get(id=game_id)
    g.play(i, j)
    g.save()
    return redirect('ttt:game', game_id)

def gameover(request, game_id):
    g = Game.objects.get(id=game_id)

    win = 'The game was tied'

    if g.winner == 1:
        win = 'Player 1 won'
        g.p1.wins += 1
        g.p2.losses += 1
        g.p1.save()
        g.p2.save()
    if g.winner == 2:
        win = 'Player 2 won'
        g.p1.losses += 1
        g.p2.wins += 1
        g.p1.save()
        g.p2.save()
    
    g.delete()

    return render(request, 'tic_tac_toe/gameover.html', {'win_str': win})

def create_user(request, name):
    p = Player()

    p.name = name
    p.save()

    return redirect('ttt:index')