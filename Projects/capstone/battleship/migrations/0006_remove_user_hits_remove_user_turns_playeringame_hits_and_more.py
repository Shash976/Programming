# Generated by Django 4.0.3 on 2022-05-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0005_map'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='user',
            name='turns',
        ),
        migrations.AddField(
            model_name='playeringame',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playeringame',
            name='turns',
            field=models.IntegerField(default=0),
        ),
    ]