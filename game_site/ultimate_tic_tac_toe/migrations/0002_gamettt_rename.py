# Manually made by Rok Strah on 2019-07-12 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ultimate_tic_tac_toe', '0001_initial'),
        ('tic_tac_toe', '0009_auto_20190710_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameuttt',
            name='g0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g0', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g1', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g2', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g3', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g4', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g5',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g5', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g6',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g6', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g7',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g7', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='g8',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_g8', to='tic_tac_toe.GameTTT'),
        ),
        migrations.AlterField(
            model_name='gameuttt',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uttt_game', to='tic_tac_toe.GameTTT'),
        ),
    ]
