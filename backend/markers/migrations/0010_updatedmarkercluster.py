# Generated by Django 4.2.5 on 2024-01-27 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0009_remove_markercluster_zoom_markercluster_square_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="UpdatedMarkerCluster",
            fields=[
                (
                    "markercluster_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="markers.markercluster",
                    ),
                ),
            ],
            bases=("markers.markercluster",),
        ),
    ]