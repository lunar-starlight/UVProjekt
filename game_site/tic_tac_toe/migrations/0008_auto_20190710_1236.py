# Generated by Django 2.2.3 on 2019-07-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tic_tac_toe', '0007_game_game_over'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='play_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='play_url',
            field=models.CharField(default='ttt:play', max_length=100),
        ),
    ]