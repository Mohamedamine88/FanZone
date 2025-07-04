# Generated by Django 5.2 on 2025-05-08 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_matchticket_match_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchticket',
            name='match_type',
            field=models.CharField(choices=[('CAN', 'CAN 2025'), ('WORLD_CUP', 'World Cup 2030'), ('GROUP_STAGE', 'Group Stage'), ('ROUND_OF_16', 'Round of 16'), ('QUARTER_FINALS', 'Quarter Finals'), ('SEMI_FINALS', 'Semi Finals'), ('FINAL', 'Final')], max_length=20),
        ),
    ]
