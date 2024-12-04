# Generated by Django 5.1.2 on 2024-12-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0024_alter_pcreservation_reserved_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='news',
            name='image_url',
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default='uploads/events/default.jpg', upload_to='uploads/events/'),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(default='uploads/news/default.jpg', upload_to='uploads/news/'),
        ),
    ]
