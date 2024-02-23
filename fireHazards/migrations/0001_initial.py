# Generated by Django 5.0.1 on 2024-01-25 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spaces', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FireHazard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.CharField(max_length=255)),
                ('hazard_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fireHazards.hazardcategory')),
            ],
        ),
        migrations.CreateModel(
            name='UserFireHazard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_image', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255)),
                ('capture_time', models.DateTimeField()),
                ('fire_hazard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fireHazards.firehazard')),
                ('my_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.myspace')),
            ],
        ),
    ]
