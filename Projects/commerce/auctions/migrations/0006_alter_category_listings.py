# Generated by Django 4.0.1 on 2022-02-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='listings',
            field=models.ManyToManyField(related_name='categories', to='auctions.Listing'),
        ),
    ]
