# Generated by Django 4.2.5 on 2023-11-06 09:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0004_alter_story_marker"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="story",
            name="author",
        ),
        migrations.RemoveField(
            model_name="story",
            name="text",
        ),
    ]
