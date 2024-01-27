# Generated by Django 4.2.5 on 2024-01-27 14:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0011_remove_updatedmarkercluster_markercluster_ptr_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MarkerCluster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("square_size", models.FloatField()),
                ("markers_count", models.PositiveIntegerField()),
                (
                    "update_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Update date"),
                ),
            ],
            options={
                "verbose_name_plural": "Marker Clusters",
            },
        ),
        migrations.CreateModel(
            name="UpdatedMarkerCluster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("square_size", models.FloatField()),
                ("markers_count", models.PositiveIntegerField()),
                (
                    "update_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Update date"),
                ),
            ],
            options={
                "verbose_name_plural": "Updated Marker Clusters",
            },
        ),
    ]