# Generated by Django 4.2.5 on 2024-03-24 15:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_marker_kind_alter_markerkind_kind_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MarkerKind",
        ),
    ]
