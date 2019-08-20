# Generated by Django 2.2.4 on 2019-08-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tic_tac_toe', '0003_negamaxtttai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamettt',
            name='keep_score',
            field=models.BooleanField(default=True, verbose_name='keep_score'),
        ),
        migrations.AlterField(
            model_name='gamettt',
            name='play_id',
            field=models.IntegerField(default=0, verbose_name='play_id'),
        ),
        migrations.AlterField(
            model_name='gamettt',
            name='play_url',
            field=models.CharField(default='ttt:play', max_length=100, verbose_name='play_url'),
        ),
    ]
