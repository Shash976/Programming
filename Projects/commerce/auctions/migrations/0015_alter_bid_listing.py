# Generated by Django 4.0.3 on 2022-04-23 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_category_options_rename_user_listing_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bids', to='auctions.listing'),
        ),
    ]