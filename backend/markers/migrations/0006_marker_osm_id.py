# Generated by Django 4.2.5 on 2024-01-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0005_alter_marker_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="marker",
            name="osm_id",
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
