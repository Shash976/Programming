# Generated by Django 4.0.4 on 2022-04-25 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_listing_base_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='base_price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]