# Generated by Django 4.0.3 on 2022-05-23 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0009_alter_match_players_alter_playeringame_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_won', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='playeringame',
            name='type',
            field=models.CharField(choices=[('Winner', 'Winner'), ('Loser', 'Loser'), ('Unknown', 'Unknown')], default='UNKNOWN', max_length=7),
        ),
    ]
