# Generated by Django 4.2.2 on 2023-07-10 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_credit_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='percentage',
            field=models.CharField(choices=[('12', '1 Week'), ('20', '2 Weeks'), ('25', '25% 1Month'), ('30', '1 Month'), ('40', '8 Weeks'), ('50', '12 Weeks')], default='30', max_length=3),
        ),
    ]
