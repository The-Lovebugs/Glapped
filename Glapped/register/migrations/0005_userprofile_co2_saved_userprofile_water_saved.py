# Generated by Django 5.1.6 on 2025-03-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_alter_userprofile_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='co2_saved',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='water_saved',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
