# Generated by Django 2.2.3 on 2019-07-10 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimate_tic_tac_toe', '0001_initial'),
        ('tic_tac_toe', '0008_auto_20190710_1236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game',
            new_name='GameTTT',
        ),
    ]
