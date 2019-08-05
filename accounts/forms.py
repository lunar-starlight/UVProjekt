from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Player


class PlayerCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Player
        fields = ('username', 'email', 'first_name', 'last_name')


class PlayerChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Player
        fields = ('username', 'email', 'first_name', 'last_name')
