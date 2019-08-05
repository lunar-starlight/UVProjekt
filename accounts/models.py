from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
