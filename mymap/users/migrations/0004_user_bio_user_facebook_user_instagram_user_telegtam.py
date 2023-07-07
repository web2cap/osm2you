# Generated by Django 4.0.2 on 2022-05-14 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='bio'),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.CharField(blank=True, default=None, max_length=254, null=True, verbose_name='facebook'),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='instagram'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegtam',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='telegtam'),
        ),
    ]
