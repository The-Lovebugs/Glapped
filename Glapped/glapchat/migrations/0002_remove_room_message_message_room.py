# Generated by Django 5.1.6 on 2025-03-07 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glapchat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='message',
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='glapchat.room'),
        ),
    ]
