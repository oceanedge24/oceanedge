# Generated by Django 5.1.3 on 2025-02-01 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_revenue_share'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(help_text='Upload a PNG image.', upload_to='profile_icons/')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='selected_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.profileicon'),
        ),
    ]
