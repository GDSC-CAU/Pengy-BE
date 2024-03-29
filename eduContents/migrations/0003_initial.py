# Generated by Django 5.0.1 on 2024-02-03 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eduContents', '0002_delete_educationcontent'),
        ('fireHazards', '0002_remove_userfirehazard_capture_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='EduContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_news_data', models.JSONField()),
                ('fire_safety_instructions', models.JSONField()),
                ('youtube_video_links', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fire_hazard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fireHazards.firehazard')),
            ],
            options={
                'verbose_name': 'Educational Content',
                'verbose_name_plural': 'Educational Contents',
            },
        ),
    ]
