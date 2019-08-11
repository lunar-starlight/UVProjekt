from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import PlayerChangeForm, PlayerCreationForm


class SignUpView(generic.CreateView):
    form_class = PlayerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class EditView(LoginRequiredMixin, generic.UpdateView):
    form_class = PlayerChangeForm
    success_url = reverse_lazy('common:home')
    login_url = reverse_lazy('login')
    template_name = 'registration/edit.html'

    def get_object(self):
        return self.request.user
