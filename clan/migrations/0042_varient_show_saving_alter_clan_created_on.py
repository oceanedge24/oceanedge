# Generated by Django 5.1.3 on 2025-02-07 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0041_varient_revenue_share_alter_clan_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='varient',
            name='show_saving',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 7, 3, 38, 12, 237905)),
        ),
    ]
