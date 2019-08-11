from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('common:home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('common:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/home.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<title>Home</title>')


class LeaderboardTests(TestCase):

    def setUp(self):
        get_user_model().objects.bulk_create(
            [get_user_model()(username='dummy' + ('0' if i < 10 else '') + str(i)) for i in range(100)]
        )

    def test_leaderboard_page_status_code(self):
        response = self.client.get('/leaderboard/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('common:leaderboard'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('common:leaderboard'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/leaderboard.html')

    def test_leaderboard_page_contains_correct_html(self):
        response = self.client.get('/leaderboard/')
        self.assertContains(response, '<title> Leaderboard </title>')

    def test_leaderboard_pagination(self):
        response = self.client.get('/leaderboard/?page=5')
        self.assertContains(response, 'dummy40')
        self.assertContains(response, 'dummy49')
        self.assertNotContains(response, 'dummy39')
        self.assertNotContains(response, 'dummy50')

    def test_paginate_by(self):
        response = self.client.get('/leaderboard/?paginate_by=25')
        self.assertContains(response, 'dummy00')
        self.assertContains(response, 'dummy24')
        self.assertNotContains(response, 'dummy25')

    def test_paginate_by_page(self):
        response = self.client.get('/leaderboard/?paginate_by=15&page=3')
        self.assertContains(response, 'dummy30')
        self.assertContains(response, 'dummy44')
        self.assertNotContains(response, 'dummy29')
        self.assertNotContains(response, 'dummy45')

    def test_search(self):
        response = self.client.get('/leaderboard/?paginate_by=100&search=dum')
        for i in range(100):
            self.assertContains(response, 'dummy' + ('0' if i < 10 else '') + str(i))

    def test_search_2(self):
        response = self.client.get('/leaderboard/?paginate_by=100&search=ummy1')
        for i in range(100):
            if 10 <= i < 20:
                self.assertContains(response, 'dummy' + ('0' if i < 10 else '') + str(i))
            else:
                self.assertNotContains(response, 'dummy' + ('0' if i < 10 else '') + str(i))
