# Generated by Django 4.2.5 on 2024-02-06 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0017_delete_markerkindgroup"),
        ("tags", "0005_markerkind_markerkind_unique_kind_marker_value"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="markerkind",
            name="unique_kind_marker_value",
        ),
        migrations.AlterField(
            model_name="markerkind",
            name="marker",
            field=models.ForeignKey(
                help_text="Choice marker",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="kind",
                to="markers.marker",
                unique=True,
                verbose_name="Marker",
            ),
        ),
    ]
