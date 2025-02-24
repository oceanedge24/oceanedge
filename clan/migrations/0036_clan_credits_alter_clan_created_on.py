# Generated by Django 5.1.3 on 2025-01-26 15:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0035_alter_clan_created_on_clanpaymentloan'),
    ]

    operations = [
        migrations.AddField(
            model_name='clan',
            name='credits',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 26, 7, 39, 21, 189911)),
        ),
    ]
