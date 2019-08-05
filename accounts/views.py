from django.urls import reverse_lazy
from django.views import generic

from .forms import PlayerCreationForm


class SignUpView(generic.CreateView):
    form_class = PlayerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
