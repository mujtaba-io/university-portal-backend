# Generated by Django 5.1.2 on 2024-11-13 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0002_alter_lecture__class_alter_student__class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='time_table',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='a.timetable'),
        ),
    ]
