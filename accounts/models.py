from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Player(AbstractUser):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=200, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False)

    def won(self):
        self.wins += 1
        self.save()

    def lost(self):
        self.losses += 1
        self.save()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(' ')[0]
