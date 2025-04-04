# Generated by Django 5.1.2 on 2024-11-19 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0010_event_day_event_linkedin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_lab',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.room')),
            ],
        ),
        migrations.CreateModel(
            name='PCReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pc_reservations', to='a.pc')),
            ],
        ),
    ]
