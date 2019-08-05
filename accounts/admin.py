from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PlayerCreationForm, PlayerChangeForm
from .models import Player


class PlayerAdmin(UserAdmin):
    add_form = PlayerCreationForm
    form = PlayerChangeForm
    model = Player
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', ]


admin.site.register(Player, PlayerAdmin)
