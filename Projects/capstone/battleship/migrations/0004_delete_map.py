# Generated by Django 4.0.3 on 2022-05-23 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0003_playeringame_alter_match_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Map',
        ),
    ]