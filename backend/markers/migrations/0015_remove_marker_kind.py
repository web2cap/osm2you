# Generated by Django 4.2.5 on 2024-01-31 17:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0014_alter_marker_kind"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="marker",
            name="kind",
        ),
    ]