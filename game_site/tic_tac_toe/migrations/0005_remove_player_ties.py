# Generated by Django 2.2.3 on 2019-07-09 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tic_tac_toe', '0004_auto_20190709_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='ties',
        ),
    ]
