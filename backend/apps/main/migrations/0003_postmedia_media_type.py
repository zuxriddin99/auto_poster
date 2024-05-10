# Generated by Django 5.0.6 on 2024-05-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='media_type',
            field=models.CharField(choices=[('video', 'Video'), ('image', 'Image')], default='image', max_length=20),
        ),
    ]
