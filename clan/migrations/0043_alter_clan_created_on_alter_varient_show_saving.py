# Generated by Django 5.1.3 on 2025-02-07 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0042_varient_show_saving_alter_clan_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 7, 6, 8, 49, 909306)),
        ),
        migrations.AlterField(
            model_name='varient',
            name='show_saving',
            field=models.BooleanField(default=True),
        ),
    ]
