# Generated by Django 5.1.6 on 2025-02-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0003_userprofile_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="points",
            field=models.IntegerField(default=100),
        ),
    ]
