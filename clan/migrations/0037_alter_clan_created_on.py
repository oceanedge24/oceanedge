# Generated by Django 5.1.3 on 2025-01-26 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0036_clan_credits_alter_clan_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 26, 9, 55, 50, 209288)),
        ),
    ]
