# Generated by Django 4.0.4 on 2022-04-25 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_categories_category_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='base_price',
        ),
    ]
