# Generated by Django 5.1.2 on 2024-11-25 16:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0021_user_is_faculty_user_is_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='day',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
