from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import GameCF


class TicTacToeIndexViewTest(TestCase):

    def setUp(self):
        self.p1 = get_user_model().objects.create_user('p1')
        self.p2 = get_user_model().objects.create_user('p2')
        for _ in range(10):
            GameCF.new_game(p1=self.p1, p2=self.p2)

    def test_index_page_status_code(self):
        response = self.client.get('/cf/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('cf:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cf:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'connect_four/index.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/cf/')
        self.assertContains(response, '<title> Connect Four </title>')
        # TODO: test for table contents
