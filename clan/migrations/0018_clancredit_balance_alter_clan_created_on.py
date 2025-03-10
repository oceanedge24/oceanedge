# Generated by Django 5.1.3 on 2025-01-12 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0017_clancredit_total_amount_alter_clan_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clancredit',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 12, 2, 12, 56, 672823)),
        ),
    ]
