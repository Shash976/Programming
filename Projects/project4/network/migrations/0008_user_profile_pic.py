# Generated by Django 4.0.1 on 2022-03-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_user_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
