# Generated by Django 4.0.3 on 2022-04-30 05:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_alter_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 30, 11, 23, 29, 622094)),
        ),
    ]
