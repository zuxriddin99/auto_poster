# Generated by Django 5.0.6 on 2024-05-22 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_plannedposts_count_max_posts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramchennels',
            name='channel_name',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название канала'),
        ),
        migrations.AlterField(
            model_name='telegramchennels',
            name='channel_username',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название канала(username)'),
        ),
    ]
