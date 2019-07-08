from django.shortcuts import render, redirect

from .models import Game

def index(request):
    return render(request, 'tic_tac_toe/index.html', {})

def new_game(request):
    g = Game()
    g.save()
    return redirect(game, g.id)

def game(request, game_id):
    g = Game.objects.get(id=game_id)

    if g.winner != 0 or g.field.count('0') == 0:
        return redirect(gameover, game_id)

    conv = {'0': '', '1': 'X', '2': 'O'}

    field = [[conv[g.field[3*i + j]] for j in range(3)] for i in range(3)]

    return render(request, 'tic_tac_toe/game.html', {
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
    })

def play(request, game_id, i, j):
    g = Game.objects.get(id=game_id)
    g.play(i, j)
    g.save()
    return redirect(game, game_id)

def gameover(request, game_id):
    g = Game.objects.get(id=game_id)

    win = 'The game was tied'

    if g.winner == 1:
        win = 'Player 1 won'
    if g.winner == 2:
        win = 'Player 2 won'

    return render(request, 'tic_tac_toe/gameover.html', {'win_str': win})
