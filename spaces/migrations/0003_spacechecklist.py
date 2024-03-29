# Generated by Django 4.2.10 on 2024-02-22 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0002_myspace_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklistItem', models.CharField(max_length=255)),
                ('isCompleted', models.BooleanField(default=False)),
                ('mySpace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='spaces.myspace')),
            ],
        ),
    ]
