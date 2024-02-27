# Generated by Django 4.2.5 on 2024-02-23 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_story_story_text_min_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="RelatedMarkerScrap",
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
                (
                    "marker_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.marker"
                    ),
                ),
            ],
        ),
    ]