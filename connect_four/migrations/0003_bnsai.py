# Generated by Django 2.2.4 on 2019-08-14 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect_four', '0002_baseai_mtdfai_negamaxprunningtttai_negamaxtttai_negimaxabtablesai_principalvariationsearchai_randomc'),
    ]

    operations = [
        migrations.CreateModel(
            name='BNSAI',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('connect_four.negimaxabtablesai',),
        ),
    ]