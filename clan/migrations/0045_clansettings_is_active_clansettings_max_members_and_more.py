# Generated by Django 5.1.3 on 2025-02-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0044_alter_clan_created_on_clansettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='clansettings',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='clansettings',
            name='max_members',
            field=models.PositiveIntegerField(default=20, max_length=3),
        ),
        migrations.AlterField(
            model_name='clan',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
