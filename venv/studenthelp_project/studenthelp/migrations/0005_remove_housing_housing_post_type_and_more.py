# Generated by Django 5.0.4 on 2024-04-27 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studenthelp', '0004_alter_stage_stage_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housing',
            name='housing_post_type',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='transportation_post_type',
        ),
    ]
