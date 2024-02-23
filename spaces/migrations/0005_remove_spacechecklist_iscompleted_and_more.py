# Generated by Django 4.2.10 on 2024-02-22 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0004_remove_spacechecklist_myspace_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spacechecklist',
            name='isCompleted',
        ),
        migrations.AlterField(
            model_name='spacechecklist',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='spaces.spacecategory'),
        ),
        migrations.CreateModel(
            name='MySpaceChecklistStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isCompleted', models.BooleanField(default=False)),
                ('checklistItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='spaces.spacechecklist')),
                ('mySpace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklistStatuses', to='spaces.myspace')),
            ],
        ),
    ]