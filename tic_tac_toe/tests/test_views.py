from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import GameTTT


class TicTacToeIndexViewTest(TestCase):

    def setUp(self):
        self.p1 = get_user_model().objects.create_user('p1')
        self.p2 = get_user_model().objects.create_user('p2')
        for _ in range(10):
            GameTTT.new_game(p1=self.p1, p2=self.p2)

    def test_index_page_status_code(self):
        response = self.client.get('/ttt/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('ttt:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ttt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tic_tac_toe/index.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/ttt/')
        self.assertContains(response, '<title> Tic Tac Toe </title>')
        # TODO: test for table contents
