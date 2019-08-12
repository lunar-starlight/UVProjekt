from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import GameUTTT, GameUTTT_ChildGame
from tic_tac_toe.models import GameTTT
from common.models import DataCell


class UltimateTicTacToeModelTests(TestCase):

    def setUp(self):
        self.p1 = get_user_model().objects.create_user('p1')
        self.p2 = get_user_model().objects.create_user('p2')

    def test_new_game(self):
        game = GameUTTT.new_game(p1=self.p1, p2=self.p2)
        self.assertIsInstance(game.game, GameTTT)
        game_list = game.game_list()
        for row in game_list:
            for el in row:
                self.assertFalse(el.keep_score)

    def test_play_returns_true(self):
        game = GameUTTT.new_game(p1=self.p1, p2=self.p2)
        b = game.play(0, 0)
        self.assertTrue(b)

    def test_play_plays_as_player(self):
        game = GameUTTT.new_game(p1=self.p1, p2=self.p2)
        gm = GameUTTT_ChildGame.get_game(parent=game, row=0, col=0)

        game.play(0, 0)
        cell1 = DataCell.objects.get(id_game=gm.pk, row=0, col=0)
        self.assertEqual(cell1.data, 1)
        self.assertEqual(game.player, 2)

        game.play(0, 1)
        cell2 = DataCell.objects.get(id_game=gm.pk, row=0, col=1)
        self.assertEqual(cell2.data, 2)
        self.assertEqual(game.player, 1)

    def test_check_win(self):
        game = GameUTTT.new_game(p1=self.p1, p2=self.p2)
        game.play(0, 1)
        game.play(0, 0)
        game.play(1, 1)
        game.play(0, 0)
        game.play(2, 1)
        game.play(0, 0)

        game.play(0, 1, 1, 0)
        game.play(1, 0)
        game.play(1, 1)
        game.play(1, 0)
        game.play(2, 1)
        game.play(1, 0)

        game.play(0, 1, 2, 0)
        game.play(2, 0)
        game.play(1, 1)
        game.play(2, 0)
        game.play(2, 1)
        self.assertTrue(game.game_over)
        self.assertTrue(game.game.game_over)
        self.assertEqual(game.winner, 1)
        game_list = game.game_list()
        for row in game_list:
            for el in row:
                self.assertTrue(el.game_over)

    def test_game_list(self):
        game = GameUTTT.new_game(p1=self.p1, p2=self.p2)
        game_list = game.game_list()
        for i in range(3):
            for j in range(3):
                gm = game_list[i][j]
                self.assertIsInstance(gm, GameTTT)


class ChildGameModelTests(TestCase):
    model = GameUTTT_ChildGame

    def setUp(self):
        self.p1 = get_user_model().objects.create_user('p1')
        self.p2 = get_user_model().objects.create_user('p2')
        self.game = GameUTTT.new_game(p1=self.p1, p2=self.p2)

    def test_child_game_new_game(self):
        g = self.model.new_game(parent=self.game, i=-1, j=-1)
        self.assertIsNotNone(g)

    def test_child_game_get_game(self):
        for i in range(3):
            for j in range(3):
                g = self.model.get_game(parent=self.game, row=i, col=i)
                self.assertIsNotNone(g)
