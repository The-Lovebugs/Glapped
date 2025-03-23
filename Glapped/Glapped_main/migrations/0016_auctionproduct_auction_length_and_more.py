# Generated by Django 5.1.6 on 2025-03-06 17:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Glapped_main', '0015_auctionproduct_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionproduct',
            name='auction_length',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='auctionproduct',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
