from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404, redirect
from django.views import generic


class SearchView(generic.ListView):
    paginate_by = 10
    search_fields = None

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET and request.GET['search'] == '':
            if 'paginate_by' in request.GET:
                return redirect(request.path + '?paginate_by=' + request.GET['paginate_by'])
            else:
                return redirect(request.path)
        if 'paginate_by' in request.GET and request.GET['paginate_by'] == '':
            if 'search' in request.GET:
                return redirect(request.path + '?search=' + request.GET['search'])
            else:
                return redirect(request.path)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            if self.request.GET['search'] != '' and self.search_fields is not None:
                self.queryset = self.queryset.annotate(
                    similarity=sum(TrigramSimilarity(s, self.request.GET['search']) for s in self.search_fields)
                ).filter(similarity__gt=0.3).order_by('-similarity')
        except KeyError:
            pass
        return super().get_queryset()

    def get_paginate_by(self, queryset):
        try:
            if self.request.GET['paginate_by'] != '':
                self.paginate_by = self.request.GET['paginate_by']
        except KeyError:
            pass
        return super().get_paginate_by(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginate_by_values"] = sorted({10, 25, 100} | {int(self.paginate_by)})
        return context


class BaseIndexView(SearchView):
    template_name = None
    model = None
    queryset = None
    context_object_name = 'game_list'
    ordering = ['pk']
    search_fields = {'p2__username', 'p2__full_name'}

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return super().get_queryset()


class LeaderboardView(SearchView):
    template_name = 'common/leaderboard.html'
    ordering = ['-wins', 'losses', 'username']


@login_required
def add_friend(request, pk: int):
    friend = get_object_or_404(get_user_model(), pk=pk)
    request.user.friends.add(friend)
    request.user.save()
    return redirect('common:leaderboard')


@login_required
def remove_friend(request, pk: int):
    friend = get_object_or_404(get_user_model(), pk=pk)
    request.user.friends.remove(friend)
    request.user.save()
    return redirect('common:leaderboard')


class BaseCreateGameView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = None
    model = None

    def get_redirect_url(self, *args, **kwargs):
        p2 = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        g = self.model.new_game(p1=self.request.user, p2=p2)
        return super().get_redirect_url(*args, g.pk)


class BasePlayView(LoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    pattern_name = None
    model = None
    play_args = list()

    def get_redirect_url(self, *args, **kwargs):
        g = get_object_or_404(self.model, pk=kwargs['pk'])
        g.play(*(kwargs[s] for s in self.play_args))
        return super().get_redirect_url(*args, kwargs['pk'])

    def test_func(self):
        g: self.model = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.request.user == g.current_player()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class BaseNewGameView(LoginRequiredMixin, SearchView):
    template_name = None
    model = get_user_model()
    queryset = model.objects.all()
    ordering = ['username']
    search_fields = {'username', 'full_name'}

    def get_queryset(self):
        self.queryset = self.request.user.friends.all()
        return super().get_queryset()
