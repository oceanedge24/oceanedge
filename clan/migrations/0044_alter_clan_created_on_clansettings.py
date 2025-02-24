# Generated by Django 5.1.3 on 2025-02-20 08:57

import datetime
import django.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0043_alter_clan_created_on_alter_varient_show_saving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.CreateModel(
            name='ClanSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_can_see_credits', models.CharField(choices=[('everyone', 'Everyone'), ('staff', 'Trassurers and Chief')], default='everyone', max_length=10)),
                ('minimum_in_savings_for_credit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('maximum_member_savings', models.DecimalField(decimal_places=2, default=10000, max_digits=10)),
                ('maximum_credit', models.DecimalField(decimal_places=2, default=5000, max_digits=10)),
                ('clan', models.OneToOneField(on_delete=django.db.models.fields.CharField, to='clan.clan')),
            ],
        ),
    ]
