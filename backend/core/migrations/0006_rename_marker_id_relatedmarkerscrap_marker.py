# Generated by Django 4.2.5 on 2024-02-23 21:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_relatedmarkerscrap"),
    ]

    operations = [
        migrations.RenameField(
            model_name="relatedmarkerscrap",
            old_name="marker_id",
            new_name="marker",
        ),
    ]