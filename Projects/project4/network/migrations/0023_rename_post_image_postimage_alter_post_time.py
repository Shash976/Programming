# Generated by Django 4.0.3 on 2022-04-30 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0022_alter_post_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post_Image',
            new_name='PostImage',
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 30, 11, 57, 17, 423857)),
        ),
    ]
