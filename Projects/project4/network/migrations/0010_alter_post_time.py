# Generated by Django 4.0.1 on 2022-03-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
