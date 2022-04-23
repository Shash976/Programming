# Generated by Django 4.0.4 on 2022-04-23 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_user_listing_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user_id',
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.CharField(default='Admin', max_length=24),
            preserve_default=False,
        ),
    ]