# Generated by Django 4.2.5 on 2023-12-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("markers", "0004_alter_marker_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="marker",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
