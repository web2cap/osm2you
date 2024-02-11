# Generated by Django 4.2.5 on 2024-02-06 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tags", "0003_alter_kindgroup_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Kind",
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
                ("value", models.CharField(max_length=255)),
                (
                    "kind_group",
                    models.ForeignKey(
                        help_text="Specify kind group",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kind_tag",
                        to="tags.kindgroup",
                        verbose_name="Kind Group",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        help_text="Choice tag for describe kind",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kind_tag",
                        to="tags.tag",
                        verbose_name="Kind tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "Marker kind",
                "verbose_name_plural": "Markers kinds",
                "ordering": ("-tag", "-value"),
            },
        ),
        migrations.AddConstraint(
            model_name="kind",
            constraint=models.UniqueConstraint(
                fields=("tag", "value"), name="unique_kind_tag"
            ),
        ),
    ]
