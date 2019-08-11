from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404, redirect
from django.views import generic


class SearchView(generic.ListView):
    model = get_user_model()
    paginate_by = 10
    queryset = model.objects.all()

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
        return super().get(request, args, kwargs)

    def get_queryset(self):
        try:
            if self.request.GET['search'] != '':
                self.queryset = self.queryset.annotate(
                    similarity=TrigramSimilarity('username', self.request.GET['search'])
                    + TrigramSimilarity('full_name', self.request.GET['search'])
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
